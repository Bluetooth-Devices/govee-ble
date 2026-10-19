# Reading advertisements on Windows

An application can use [Bleak](https://bleak.readthedocs.io/) to scan with the
Windows Bluetooth adapter and pass advertisements to `govee-ble`. Scanning belongs
to the application; `govee-ble` remains a parser and does not open connections.

This example reads live H5105 thermometer/hygrometer advertisements without
pairing, GATT connections, or a Govee account. It was tested with Python 3.12,
Bleak 3.0.2, and `govee-ble` 1.5.1 on Windows. It does not download the sensor's
stored history or configure the device.

## Install in Windows Python

Run these commands in Windows PowerShell using a Windows Python installation:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "govee-ble==1.5.1" "bleak==3.0.2"
```

Use the Windows interpreter for this example, rather than a Python interpreter
inside WSL. Enable Bluetooth in Windows and place the H5105 within range.

## Read live H5105 measurements

Save the following as `read_h5105.py`:

```python
import asyncio
import json
import os

from bleak import AdvertisementData, BLEDevice, BleakScanner
from home_assistant_bluetooth import BluetoothServiceInfo

from govee_ble import GoveeBluetoothDeviceData


async def main() -> None:
    decoders: dict[str, GoveeBluetoothDeviceData] = {}
    target_address = os.environ.get("GOVEE_BLE_ADDRESS", "").upper()

    def received(device: BLEDevice, advertisement: AdvertisementData) -> None:
        if target_address and device.address.upper() != target_address:
            return
        name = advertisement.local_name or device.name or ""
        if not name.startswith("GVH5105_"):
            return

        # Keep one parser instance per sensor, as in the general usage example.
        if device.address not in decoders:
            decoders[device.address] = GoveeBluetoothDeviceData()
        service_info = BluetoothServiceInfo.from_advertisement(
            device, advertisement, "windows"
        )
        update = decoders[device.address].update(service_info)
        readings = {
            key.key: value.native_value
            for key, value in update.entity_values.items()
            if key.key in ("temperature", "humidity", "battery", "signal_strength")
            and value.native_value is not None
        }
        if all(key in readings for key in ("temperature", "humidity", "battery")):
            print(json.dumps(readings), flush=True)

    async with BleakScanner(detection_callback=received, scanning_mode="active"):
        await asyncio.sleep(30)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
```

Run it from the same PowerShell window:

```powershell
.\.venv\Scripts\python.exe .\read_h5105.py
```

The scanner runs for 30 seconds and prints JSON readings for nearby sensors whose
advertised name starts with `GVH5105_`. Temperature is in degrees Celsius, humidity
and battery are percentages, and signal strength is in dBm when present. Press
Ctrl+C to stop early. No output means no matching, decodable measurements arrived
during that interval; check Bluetooth, distance, and the advertised model name.

To restrict scanning results to one sensor, optionally set `GOVEE_BLE_ADDRESS` to
its Bluetooth MAC address in the local PowerShell environment before running the
script. Keep that value private. The example prints readings without device names
or addresses, but measurements can still reveal information about a home; review
output before sharing it.

This example targets H5105 advertisements. Other supported models can use the
same scanner-to-parser pattern, with an appropriate device filter. It is not a
background service and has no automatic restart or stale-data handling.

## When Home Assistant runs in WSL

If Windows needs to retain its Bluetooth adapter for peripherals, a Windows
receiver can keep scanning there while Home Assistant runs in WSL. In the tested
setup, the adapter continued serving existing Bluetooth peripherals while
receiving sensor advertisements; no adapter passthrough was used.

A separate application can forward decoded readings through a local MQTT broker
to Home Assistant's [MQTT integration](https://www.home-assistant.io/integrations/mqtt/).
The application must implement MQTT discovery or configure the sensors, publish
availability, and expire stale readings. The short example above only decodes
advertisements; it does not provide these bridge features. Broker authentication
and network exposure must be configured for the deployment.

When Home Assistant can access Bluetooth directly, prefer its built-in
[Govee Bluetooth integration](https://www.home-assistant.io/integrations/govee_ble/).
The Windows receiver pattern is an alternative for a host where the adapter stays
with Windows, not an additional requirement for the native integration.
