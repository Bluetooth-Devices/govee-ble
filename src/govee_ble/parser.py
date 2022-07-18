"""Parser for Govee BLE advertisements.

This file is shamlessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""
from __future__ import annotations

import logging
import struct
from abc import abstractmethod

from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary, SensorUpdate
from sensor_state_data.data import DeviceClass, SensorData
from sensor_state_data.units import SIGNAL_STRENGTH_DECIBELS_MILLIWATT, TEMP_CELSIUS

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


class BluetoothData(SensorData):
    """Update bluetooth data."""

    @abstractmethod
    def update(self, data: BluetoothServiceInfo) -> None:
        """Update the data."""

    def supported(self, data: BluetoothServiceInfo) -> bool:
        """Return True if the device is supported."""
        self.generate_update(data)
        return bool(self._device_id_to_type)

    def generate_update(self, data: BluetoothServiceInfo) -> SensorUpdate:
        """Update a bluetooth device."""
        self.update_rssi(data.rssi)
        return super().generate_update(data)

    def update_rssi(self, native_value: int | float) -> None:
        """Quick update for an rssi sensor."""
        self.update_sensor(
            key="rssi",
            native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            native_value=native_value,
            device_class=DeviceClass.SIGNAL_STRENGTH,
        )


class GoveeBluetoothDeviceData(BluetoothData):
    """Data for Govee BLE sensors."""

    def update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Govee BLE advertisement data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data

        if service_info.name.startswith("GV"):
            self.set_device_name(service_info.name[2:])

        for mgr_id, mfr_data in manufacturer_data.items():
            if mgr_id in NOT_GOVEE_MANUFACTURER:
                continue
            self._process_update(mgr_id, mfr_data)

    def _process_update(self, mgr_id: int, data: bytes) -> None:
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
            device_id = "indoor"
            if sensor_id == 0:
                self.set_device_type("H5178", device_id)
            elif sensor_id == 1:
                device_id = "outdoor"
                self.set_device_type("H5178-outdoor", device_id)
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
            self.update_sensor(
                key="temperature_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_probe_1),
                name="Temperature Probe 1",
            )
            self.update_sensor(
                key="temperature_alarm_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_alarm_1),
                name="Temperature Alarm Probe 1",
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
            self.update_sensor(
                key="temperature_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_probe_1),
                name="Temperature Probe 1",
            )
            self.update_sensor(
                key="temperature_alarm_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_alarm_1),
                name="Temperature Alarm Probe 1",
            )
            self.update_sensor(
                key="temperature_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_probe_2),
                name="Temperature Probe 2",
            )
            self.update_sensor(
                key="temperature_alarm_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_alarm_2),
                name="Temperature Alarm Probe 2",
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
            self.update_sensor(
                key="temperature_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_probe_1),
                name="Temperature Probe 1",
            )
            self.update_sensor(
                key="temperature_alarm_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_alarm_1),
                name="Temperature Alarm Probe 1",
            )
            self.update_sensor(
                key="temperature_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_probe_2),
                name="Temperature Probe 2",
            )
            self.update_sensor(
                key="temperature_alarm_probe_1",
                native_unit_of_measurement=TEMP_CELSIUS,
                native_value=decode_temps_probes(temp_alarm_2),
                name="Temperature Alarm Probe 2",
            )
            return
