# Scans for Govee H5075 devices and prints their decoded data to the terminal
import asyncio
from bleak import BleakScanner

def detection_callback(device, advertisement_data):
    # Protocol decoded: https://github.com/Thrilleratplay/GoveeWatcher

    # The "friendly name" that you normally see when pairing with the device
    devname = advertisement_data.local_name
    # Estimated signal quality in dBm
    rssi = advertisement_data.rssi

    # If this is a GVH5075 family device, decode the message
    if devname and "GVH507" in devname:
        payload = advertisement_data.manufacturer_data[60552][1:5]

        # last byte in payload is the battery percentage, as an 8-bit int
        batt = int(payload[-1])
        
        # temperature and humidity are combined in a 24-bit int
        temphum = int.from_bytes(payload[0:3], "big")

        # uppermost bit is the sign, so we record its state...
        isNegative = (temphum & 0x800000) != 0
        # ... and remove it from further calculations
        temphum &= ~(0x800000)

        # humidity in 10ths of a percent is the last three digits
        hum10 = temphum % 1000
        hum = hum10 / 10
        
        # temperature is all the other digits, plus the sign information
        temp = (temphum - hum10)/10000
        if isNegative:
            temp *= -1

        print("{0}: {1}°C, {2}%, batt: {3}%, RSSI: {4}" 
              .format(advertisement_data.local_name, 
                      temp, hum, batt, rssi))
async def main():
    # Initiate a BLE scan with 20s timeout
    scanner = BleakScanner(detection_callback, timeout=20.0)
    await scanner.start()
    # Sleep while the BLE scan is happening
    await asyncio.sleep(20.0)
    await scanner.stop()

asyncio.run(main())
