import pywinusb.hid as hid
import matplotlib.pyplot as plt
import socket
import struct
import threading
import time

# HID Device Info
VID = 0x0EB7
PID = 0x4

# M5BugC2 UDP Config
UDP_IP = "192.168.1.136"  # M5BugC2 IP Address
UDP_PORT = 12345         # M5BugC2 Port

# Global Variables
accel = 0
brake = 0
steering = 0

def read_hid_data():
    global accel, brake, steering

    def data_handler(data):
        global accel, brake, steering
        accel = (data[20] << 8) | data[21]
        brake = (data[22] << 8) | data[23]
        steering = (data[18] << 8) | data[19]

    # Find HID device
    all_devices = hid.HidDeviceFilter(vendor_id=VID, product_id=PID).get_devices()
    if not all_devices:
        print("No HID device found.")
        return

    device = all_devices[0]
    device.open()
    device.set_raw_data_handler(data_handler)

    print("HID device connected. Reading data...")
    try:
        while True:
            time.sleep(0.1)  # Keep thread alive
    except KeyboardInterrupt:
        print("Stopping HID data reading.")
        device.close()


def plot_data():
    global accel, brake, steering

    plt.ion()
    fig, ax = plt.subplots()
    bars = ax.bar(['Accel', 'Brake', 'Steering'], [0, 0, 0])
    ax.set_ylim(0, 65535)

    while True:
        try:
            bars[0].set_height(accel)
            bars[1].set_height(brake)
            bars[2].set_height(steering)
            plt.pause(0.1)
        except KeyboardInterrupt:
            print("Stopping graph plot.")
            break


def send_udp_data():
    global accel, brake, steering
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            data = struct.pack('>HHH', accel, brake, steering)
            sock.sendto(data, (UDP_IP, UDP_PORT))
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping UDP transmission.")
            break


def main():
    # Start threads for each task
    threads = [
        threading.Thread(target=read_hid_data, daemon=True),
        threading.Thread(target=plot_data, daemon=True),
        threading.Thread(target=send_udp_data, daemon=True)
    ]

    for thread in threads:
        thread.start()

    try:
        while True:
            time.sleep(1)  # Main thread stays alive
    except KeyboardInterrupt:
        print("Exiting program.")


if __name__ == "__main__":
    main()
