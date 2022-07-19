"""Parser for Govee BLE advertisements.

This file is shamlessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""
from __future__ import annotations

import logging
import struct

from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary

_LOGGER = logging.getLogger(__name__)

PACKED_hHB = struct.Struct(">hHB")
PACKED_hh = struct.Struct(">hh")
PACKED_hhbhh = struct.Struct(">hhbhh")
PACKED_hhhhh = struct.Struct(">hhhhh")


NOT_GOVEE_MANUFACTURER = {76}


def decode_temps(packet_value: int) -> float:
    """Decode potential negative temperatures."""
    # https://github.com/Thrilleratplay/GoveeWatcher/issues/2
    if packet_value & 0x800000:
        return float((packet_value ^ 0x800000) / -10000)
    return float(packet_value / 10000)


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
        local_name = service_info.name
        self.set_device_manufacturer("Govee")

        if local_name.startswith("GV"):
            self.set_device_name(service_info.name[2:])

        for mfr_id, mfr_data in manufacturer_data.items():
            if mfr_id in NOT_GOVEE_MANUFACTURER:
                continue
            self._process_mfr_data(local_name, mfr_id, mfr_data)

    def _process_mfr_data(self, local_name: str, mgr_id: int, data: bytes) -> None:
        """Parser for Govee sensors."""
        _LOGGER.debug("Parsing Govee sensor: %s %s", mgr_id, data)
        msg_length = len(data)
        if msg_length > 25 and b"INTELLI_ROCKS" in data:
            # INTELLI_ROCKS sometimes ends up glued on to the end of the message
            data = data[:-25]
            msg_length = len(data)
            _LOGGER.debug("Cleaned up packet: %s %s", mgr_id, data)

        if msg_length == 6 and mgr_id == 0xEC88:
            self.set_device_type("H5072/H5075")
            packet_5072_5075 = data[1:4].hex()
            packet = int(packet_5072_5075, 16)
            temp = decode_temps(packet)
            humi = float((packet % 1000) / 10)
            batt = int(data[4])
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE, temp)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY, humi)
            self.update_predefined_sensor(SensorLibrary.BATTERY, batt)
            return

        if msg_length == 6 and mgr_id == 0x0001:
            self.set_device_type("H5101/H5102/H5177")
            packet_5101_5102 = data[2:5].hex()
            packet = int(packet_5101_5102, 16)
            temp = decode_temps(packet)
            humi = float((packet % 1000) / 10)
            batt = int(data[5])
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE, temp)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY, humi)
            self.update_predefined_sensor(SensorLibrary.BATTERY, batt)
            return

        if msg_length == 7 and mgr_id == 0xEC88:
            self.set_device_type("H5074")
            (temp, humi, batt) = PACKED_hHB.unpack(data[1:6])
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE, temp / 100)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY, humi / 100)
            self.update_predefined_sensor(SensorLibrary.BATTERY, batt)
            return

        if msg_length == 9 and mgr_id == 0xEC88:
            self.set_device_type("H5051/H5071")
            (temp, humi, batt) = PACKED_hHB.unpack(data[1:6])
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE, temp / 100)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY, humi / 100)
            self.update_predefined_sensor(SensorLibrary.BATTERY, batt)
            return

        if msg_length == 9 and mgr_id == 0x0001:
            packet_5178 = data[3:6].hex()
            packet = int(packet_5178, 16)
            temp = decode_temps(packet)
            humi = float((packet % 1000) / 10)
            batt = int(data[6])
            sensor_id = data[2]
            device_id = "primary"
            if local_name.startswith("H5178") or local_name.startswith("B5178"):
                self.set_title(local_name)
            else:
                self.set_title("H5178")
            if sensor_id == 0:
                self.set_device_name(f"{local_name} Primary", device_id)
                self.set_device_type("H5178", device_id)
                self.set_device_manufacturer("Govee", device_id)
            elif sensor_id == 1:
                device_id = "remote"
                self.set_device_name(f"{local_name} Remote", device_id)
                self.set_device_type("H5178-REMOTE", device_id)
                self.set_device_manufacturer("Govee", device_id)
            else:
                _LOGGER.debug(
                    "Unknown sensor id for Govee H5178,"
                    " please report to the developers, data: %s",
                    data.hex(),
                )
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE, temp, device_id=device_id
            )
            self.update_predefined_sensor(
                SensorLibrary.HUMIDITY, humi, device_id=device_id
            )
            self.update_predefined_sensor(
                SensorLibrary.BATTERY, batt, device_id=device_id
            )
            return

        if msg_length == 9 and mgr_id == 0x8801:
            self.set_device_type("H5179")
            (temp, humi, batt) = PACKED_hHB.unpack(data[4:9])
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE, temp / 100)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY, humi / 100)
            self.update_predefined_sensor(SensorLibrary.BATTERY, batt)
            return

        if msg_length == 14:
            self.set_device_type("H5183")
            (temp_probe_1, temp_alarm_1) = PACKED_hh.unpack(data[8:12])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            return

        if msg_length == 17:
            self.set_device_type("H5182")
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

        if msg_length == 20:
            self.set_device_type("H5185")
            (
                temp_probe_1,
                temp_alarm_1,
                _,
                temp_probe_2,
                temp_alarm_2,
            ) = PACKED_hhhhh.unpack(data[8:17])
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_1), decode_temps_probes(temp_alarm_1), 1
            )
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_2), decode_temps_probes(temp_alarm_2), 2
            )
            return

    def update_temp_probe_with_alarm(
        self, temp: float, alarm_temp: float, probe_id: int
    ) -> None:
        """Update the temperature probe with the alarm temperature."""
        self.update_predefined_sensor(
            SensorLibrary.TEMPERATURE,
            temp,
            key=f"temperature_probe_{probe_id}",
            name=f"Temperature Probe {probe_id}",
        )
        self.update_predefined_sensor(
            SensorLibrary.TEMPERATURE,
            alarm_temp,
            key=f"temperature_alarm_probe_{probe_id}",
            name=f"Temperature Alarm Probe {probe_id}",
        )
