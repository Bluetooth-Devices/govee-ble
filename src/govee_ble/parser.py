"""Parser for Govee BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""
from __future__ import annotations

import logging
import struct

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary

_LOGGER = logging.getLogger(__name__)


PACKED_hHB_LITTLE = struct.Struct("<hHB")
PACKED_hHB = struct.Struct(">hHB")
PACKED_hh = struct.Struct(">hh")

PACKED_hhbhh = struct.Struct(">hhbhh")
PACKED_hhhhh = struct.Struct(">hhhhh")


MIN_TEMP = -17.7778
MAX_TEMP = 100

NOT_GOVEE_MANUFACTURER = {76}


def decode_temp_humid(temp_humid_bytes: bytes) -> tuple[float, float]:
    """Decode potential negative temperatures."""
    base_num = (
        (temp_humid_bytes[0] << 16) + (temp_humid_bytes[1] << 8) + temp_humid_bytes[2]
    )
    is_negative = base_num & 0x800000
    temp_as_int = base_num & 0x7FFFFF
    temp_as_float = temp_as_int / 10000.0
    if is_negative:
        temp_as_float = -temp_as_float
    humid = (temp_as_int % 1000) / 10.0
    return temp_as_float, humid


def decode_temps_probes(packet_value: int) -> float:
    """Filter potential negative temperatures."""
    if packet_value < 0:
        return 0.0
    return float(packet_value / 100)


class GoveeBluetoothDeviceData(BluetoothData):
    """Data for Govee BLE sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Govee BLE advertisement data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data
        service_uuids = service_info.service_uuids
        local_name = service_info.name
        address = service_info.address
        self.set_device_manufacturer("Govee")

        if local_name.startswith("Govee_"):
            self.set_device_name(service_info.name[6:].replace("_", " "))

        if local_name.startswith("GV"):
            self.set_device_name(service_info.name[2:].replace("_", " "))

        self.set_precision(2)

        for mfr_id, mfr_data in manufacturer_data.items():
            if mfr_id in NOT_GOVEE_MANUFACTURER:
                continue
            self._process_mfr_data(address, local_name, mfr_id, mfr_data, service_uuids)

    def _process_mfr_data(
        self,
        address: str,
        local_name: str,
        mgr_id: int,
        data: bytes,
        service_uuids: list[str],
    ) -> None:
        """Parser for Govee sensors."""
        _LOGGER.debug("Parsing Govee sensor: %s %s", mgr_id, data)
        msg_length = len(data)
        if msg_length > 25 and b"INTELLI_ROCKS" in data:
            # INTELLI_ROCKS sometimes ends up glued on to the end of the message
            data = data[:-25]
            msg_length = len(data)
            _LOGGER.debug("Cleaned up packet: %s %s", mgr_id, data)

        if msg_length == 6 and (
            "H5072" in local_name or "H5075" in local_name or mgr_id == 0xEC88
        ):
            self.set_device_type("H5072/H5075")
            temp, humi = decode_temp_humid(data[1:4])
            batt = int(data[4])
            if temp >= MIN_TEMP and temp <= MAX_TEMP:
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi)
                self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length == 6 and (
            "H5101" in local_name
            or "H5102" in local_name
            or "H5177" in local_name
            or mgr_id == 0x0001
        ):
            self.set_device_type("H5101/H5102/H5177")
            temp, humi = decode_temp_humid(data[2:5])
            batt = int(data[5])
            if temp >= MIN_TEMP and temp <= MAX_TEMP:
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi)
                self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length == 7 and ("H5074" in local_name or mgr_id == 0xEC88):
            self.set_device_type("H5074")
            (temp, humi, batt) = PACKED_hHB_LITTLE.unpack(data[1:6])
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS, temp / 100
            )
            self.update_predefined_sensor(
                SensorLibrary.HUMIDITY__PERCENTAGE, humi / 100
            )
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if (
            msg_length == 9
            and mgr_id == 0xEC88
            and ("H5071" in local_name or "H5052" in local_name)
        ):
            if "H5071" in local_name:
                self.set_device_type("H5071")
            else:
                self.set_device_type("H5052")
            (temp, humi, batt) = PACKED_hHB_LITTLE.unpack(data[1:6])
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS, temp / 100
            )
            self.update_predefined_sensor(
                SensorLibrary.HUMIDITY__PERCENTAGE, humi / 100
            )
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length == 9 and (
            "H5051" in local_name or "H5071" in local_name or mgr_id == 0xEC88
        ):
            self.set_device_type("H5051/H5071")
            (temp, humi, batt) = PACKED_hHB.unpack(data[1:6])
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS, temp / 100
            )
            self.update_predefined_sensor(
                SensorLibrary.HUMIDITY__PERCENTAGE, humi / 100
            )
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length == 9 and (
            "H5178" in local_name or "B5178" in local_name or mgr_id == 0x0001
        ):
            temp, humi = decode_temp_humid(data[3:5])
            batt = int(data[6])
            sensor_id = data[2]
            device_id = "primary"
            if local_name.startswith("H5178") or local_name.startswith("B5178"):
                self.set_title(local_name)
            else:
                self.set_title("H5178")
            if sensor_id == 0:
                self.set_device_name(
                    f"{local_name} Primary".replace("_", " "), device_id
                )
                self.set_device_type("H5178", device_id)
                self.set_device_manufacturer("Govee", device_id)
            elif sensor_id == 1:
                device_id = "remote"
                self.set_device_name(
                    f"{local_name} Remote".replace("_", " "), device_id
                )
                self.set_device_type("H5178-REMOTE", device_id)
                self.set_device_manufacturer("Govee", device_id)
            else:
                _LOGGER.debug(
                    "Unknown sensor id for Govee H5178,"
                    " please report to the developers, data: %s",
                    data.hex(),
                )
            if temp >= MIN_TEMP and temp <= MAX_TEMP:
                self.update_predefined_sensor(
                    SensorLibrary.TEMPERATURE__CELSIUS, temp, device_id=device_id
                )
                self.update_predefined_sensor(
                    SensorLibrary.HUMIDITY__PERCENTAGE, humi, device_id=device_id
                )
                self.update_predefined_sensor(
                    SensorLibrary.BATTERY__PERCENTAGE, batt, device_id=device_id
                )
            return

        if msg_length == 9 and ("H5179" in local_name or mgr_id == 0x8801):
            self.set_device_type("H5179")
            temp, humi, batt = PACKED_hHB_LITTLE.unpack(data[4:9])
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS, temp / 100
            )
            self.update_predefined_sensor(
                SensorLibrary.HUMIDITY__PERCENTAGE, humi / 100
            )
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length == 14 and (
            "H5181" in local_name
            or mgr_id in {0xF861, 0x388A, 0xEA42, 0xAAA2, 0xD14B}
            or "00008151-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            self.set_device_type("H5181")
            self.set_device_name(f"H5181 {short_address(address)}")
            (temp_probe_1, temp_alarm_1) = PACKED_hh.unpack(data[8:12])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            return

        if msg_length == 17 and (
            "H5182" in local_name
            or mgr_id == 0x2730
            or "00008251-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            self.set_device_type("H5182")
            self.set_device_name(f"H5182 {short_address(address)}")
            (
                temp_probe_1,
                temp_alarm_1,
                _,
                temp_probe_2,
                temp_alarm_2,
            ) = PACKED_hhbhh.unpack(data[8:17])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_2), decode_temps_probes(temp_alarm_2), 2
            )
            return

        if msg_length == 14 and (
            "H5183" in local_name
            or mgr_id in {0x67DD, 0xE02F, 0xF79F}
            or "00008351-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            self.set_device_type("H5183")
            self.set_device_name(f"H5183 {short_address(address)}")
            (temp_probe_1, temp_alarm_1) = PACKED_hh.unpack(data[8:12])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            return

        if msg_length == 17 and (
            "H5184" in local_name
            or mgr_id == 0x1B36
            or "00008451-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            sensor_id = data[6]
            self.set_device_type("H5184")
            self.set_device_name(f"H5184 {short_address(address)}")
            (
                temp_probe_first,
                temp_alarm_first,
                _,
                temp_probe_second,
                temp_alarm_second,
            ) = PACKED_hhbhh.unpack(data[8:17])
            if sensor_id == 1:
                ids = [1, 2]
            elif sensor_id == 2:
                ids = [3, 4]
            else:
                _LOGGER.debug(
                    "Unknown sensor id: %s for a H5184, data: %s", sensor_id, data
                )
                return
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_first),
                decode_temps_probes(temp_alarm_first),
                ids[0],
            )
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_second),
                decode_temps_probes(temp_alarm_second),
                ids[1],
            )
            return

        if msg_length == 20 and (
            "H5185" in local_name
            or mgr_id in (0x4A32, 0x332, 0x4C32)
            or "00008551-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            self.set_device_type("H5185")
            self.set_device_name(f"H5185 {short_address(address)}")
            (
                temp_probe_1,
                temp_alarm_1,
                _,
                temp_probe_2,
                temp_alarm_2,
            ) = PACKED_hhhhh.unpack(data[8:18])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_2), decode_temps_probes(temp_alarm_2), 2
            )
            return

    def update_temp_probe(self, temp: float, probe_id: int) -> None:
        """Update the temperature probe with the alarm temperature."""
        self.update_predefined_sensor(
            SensorLibrary.TEMPERATURE__CELSIUS,
            temp,
            key=f"temperature_probe_{probe_id}",
            name=f"Temperature Probe {probe_id}",
        )

    def update_temp_probe_with_alarm(
        self, temp: float, alarm_temp: float, probe_id: int
    ) -> None:
        """Update the temperature probe with the alarm temperature."""
        self.update_temp_probe(temp, probe_id)
        self.update_predefined_sensor(
            SensorLibrary.TEMPERATURE__CELSIUS,
            alarm_temp,
            key=f"temperature_alarm_probe_{probe_id}",
            name=f"Temperature Alarm Probe {probe_id}",
        )
