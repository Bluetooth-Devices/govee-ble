# Usage

`govee-ble` is a stateless parser for Govee Bluetooth Low Energy
advertisement payloads. It does **not** scan for devices or open
connections — feed it raw advertisement data and it returns a
[`SensorUpdate`](https://github.com/Bluetooth-Devices/sensor-state-data)
describing what was decoded.

## Quick start

```python
from bluetooth_sensor_state_data import BluetoothServiceInfo
from govee_ble import GoveeBluetoothDeviceData

service_info = BluetoothServiceInfo(
    name="GVH5075_2762",
    address="A4:C1:38:00:00:00",
    rssi=-63,
    manufacturer_data={
        60552: b"\x00\x03A\xc2d\x00L\x00\x02\x15INTELLI_ROCKS_HW"
        b"Pu\xf2\xff\x0c"
    },
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

device = GoveeBluetoothDeviceData()
update = device.update(service_info)

for description in update.entity_descriptions.values():
    value = update.entity_values[description.device_key]
    print(description.device_key.key, value.native_value)
```

`device.update()` accepts a `BluetoothServiceInfo` for every
advertisement seen for a given MAC. Reuse the same
`GoveeBluetoothDeviceData` instance per device — readings from
multi-packet protocols (e.g. the H5178 primary/remote pair) are
accumulated on the instance.

## Inspecting a device

After at least one successful `update()`, the instance exposes:

| Attribute             | Description                                                                                               |
| --------------------- | --------------------------------------------------------------------------------------------------------- |
| `device.device_type`  | Govee model id, e.g. `"H5075"`. `None` until the first packet is decoded.                                 |
| `device.sensor_type`  | A `SensorType` enum: `THERMOMETER`, `BUTTON`, `MOTION`, `WINDOW`, `VIBRATION`, `PRESENCE`, or `PRESSURE`. |
| `device.button_count` | Number of buttons, for button-bearing models.                                                             |
| `device.sleepy`       | `True` for battery-powered sleep-and-wake devices that only advertise on events.                          |

`get_model_info(model_id)` returns the same metadata without needing
an instance:

```python
from govee_ble import get_model_info, SensorType

info = get_model_info("H5121")
assert info.sensor_type is SensorType.MOTION
assert info.sleepy is True
```

## Supported devices

The parser decodes ~30 Govee BLE models across several categories:

- **Thermometers / hygrometers** — H5051, H5052, H5055, H5071, H5072,
  H5074, H5075, H5100, H5101, H5102, H5103, H5104, H5105, H5106,
  H5108, H5174, H5177, H5179, GV5179
- **Multi-probe thermometers** — H5110, H5112 (dual probe)
- **BBQ probes** — H5181, H5182, H5183, H5184, H5185, H5191, H5198
  (up to four probes per device with high/low alarm temperatures)
- **Thermometer + hygrometer with remote sensor** — H5178 (primary +
  remote)
- **Temperature / humidity / CO₂** — H5140
- **Motion / occupancy** — H5121, H5127
- **Door / window** — H5123
- **Vibration** — H5124
- **Buttons** — H5122 (1 button), H5125 (6 buttons), H5126 (2 buttons)
- **Pressure pad** — H5130

The encrypted H512x family (H5121–H5126, H5130) advertises a CRC-checked
24-byte payload; the parser drops packets that fail the CRC check.

## Integration with Home Assistant

`govee-ble` is the parser library behind Home Assistant's
[`govee_ble` integration](https://www.home-assistant.io/integrations/govee_ble/).
In Home Assistant, advertisement bytes arrive via the Bluetooth
integration; you generally do not need to call `govee-ble` directly.
For external scripts and other consumers, the API shown above is the
full surface.
