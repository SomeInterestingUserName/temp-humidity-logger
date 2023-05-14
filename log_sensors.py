# When run, scans for Govee temperature/humidity sensors and records at most one measurement from each sensor it detects.
import asyncio
import time
from bleak import BleakScanner

# Put the path of your log file here
logfile = ""

# Keeps a record of sensors we've heard from already, so we should only get a single log entry per device.
hasReceived = {}
def detection_callback(device, advertisement_data):
    # Protocol decoded: https://github.com/Thrilleratplay/GoveeWatcher
    if device.address.startswith("A4:C1:38"):
        global hasReceived
        payload = advertisement_data.manufacturer_data[60552][1:5]
        devicename = advertisement_data.local_name
        if not hasReceived.get(devicename, False):
            batt = int(payload[-1])
            temphum = int.from_bytes(payload[0:3], "big")
            hum10 = temphum % 1000
            temp = (temphum - hum10)/10000
            hum = hum10 / 10
            with open("logfile", "a") as f:
                f.write("{0},{1},{2},{3},{4}\n".format(int(time.time()),devicename, temp, hum, batt))
            hasReceived[devicename] = True

async def main():
    global hasReceived
    if not logfile:
        raise RuntimeError("No log file provided! Please set the \"logfile\" variable in this file to your log file path.")
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    # Wait 20s to have enough time to receive temp sensor advertisements
    await asyncio.sleep(20)
    await scanner.stop()

asyncio.run(main())

