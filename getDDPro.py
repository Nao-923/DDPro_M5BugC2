import pywinusb.hid as hid

def list_hid_devices():
    # 接続されているHIDデバイスを一覧表示
    all_devices = hid.HidDeviceFilter().get_devices()
    if not all_devices:
        print("No HID devices found.")
        return

    print("Connected HID devices:")
    for device in all_devices:
        try:
            print(f"Vendor ID: {hex(device.vendor_id)}, Product ID: {hex(device.product_id)}, "
                  f"Product Name: {device.product_name}, Serial: {device.serial_number}")
        except Exception as e:
            print(f"Error reading device info: {e}")

def find_device(vid, pid):
    # 特定のVIDとPIDを持つデバイスを検索
    target_device = None
    all_devices = hid.HidDeviceFilter(vendor_id=vid, product_id=pid).get_devices()
    if all_devices:
        target_device = all_devices[0]
        print(f"Found device: {target_device.product_name} (VID: {hex(vid)}, PID: {hex(pid)})")
    else:
        print(f"Device with VID={hex(vid)} and PID={hex(pid)} not found.")
    return target_device

if __name__ == "__main__":
    # すべてのHIDデバイスをリストアップ
    list_hid_devices()

    # ハンコンのVIDとPIDを指定してデバイスを検索
    VID = 0x0eb7
    PID = 0x4
    device = find_device(VID, PID)

    if device:
        print("Device is ready for further processing.")
    else:
        print("Please ensure the device is connected and try again.")
