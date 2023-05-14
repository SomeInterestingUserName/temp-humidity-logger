# temp-humidity-logger
Scripts for receiving and logging BLE broadcasts from the Govee H5075 temperature/humidity sensors. These sensors periodically send out BLE broadcasts with temperature, humidity, and battery status. We can "sniff" for these messages and keep a log of their values. The main advantage of this method is that the sensors broadcast regardless of whether something is listening, so it has no impact on their battery life. This is in contrast to connecting directly to the sensors and either querying their sensor values or requesting a download of stored data, which requires that they open an active connection to your device. 

## Files
* `scan_ble.py` : Scans for BLE advertisements for 20s and prints out decoded data for any H5075 sensors it detects.
* `log_sensors.py` : Appends at most one sensor measurement for each H5075 sensor it detects within a 20-second window to a log file. Be sure to change the log file path to fit your needs.

## Running the Logging Script Periodically
On Linux, you can set up a `cron` job to log sensor measurements at a certain interval. For instance, you can put this in your `/etc/crontab` file to record every 15th minute of the hour (X:00, X:15, X:30, X:45):

```*/15  *    * * * [username] python3 [path_to_log_sensors.py]/log_sensors.py```

## What You'll Need
* A laptop or computer with a wireless card that supports Bluetooth Low Energy (BLE)
* A Python installation with the `bleak` library installed
* (optional) A cloud file-syncing service to back up your log file

## Thanks
* [Thrilleratplay/GoveeWatcher](https://github.com/Thrilleratplay/GoveeWatcher) for decoding the BLE data
* [Bleak Documentation](https://bleak.readthedocs.io/en/latest/) for the BLE library this project depends on
