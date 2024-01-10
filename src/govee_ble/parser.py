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
PACKED_hhhchhh_LITTLE = struct.Struct("<hhhchhh")

PACKED_hhbhh = struct.Struct(">hhbhh")
PACKED_hhhhh = struct.Struct(">hhhhh")
PACKED_hhhhhh = struct.Struct(">hhhhhh")


ERROR = "error"

MIN_TEMP = -30
MAX_TEMP = 100

NOT_GOVEE_MANUFACTURER = {76}

PROBE_MAPPING_1_2 = [1, 2]
PROBE_MAPPING_3_4 = [3, 4]

FOUR_PROBES_MAPPING = {
    sensor_id: PROBE_MAPPING_1_2 for sensor_id in (0x01, 0x41, 0x81, 0xC1)
} | {sensor_id: PROBE_MAPPING_3_4 for sensor_id in (0x02, 0x42, 0x82, 0xC2)}

SIX_PROBES_MAPPING = {
    0: [[1, 0x01], [2, 0x02]],
    64: [[3, 0x04], [4, 0x08]],
    128: [[5, 0x10], [6, 0x20]],
}


def decode_temp_humid(temp_humid_bytes: bytes) -> tuple[float, float]:
    """Decode potential negative temperatures."""
    base_num = (
        (temp_humid_bytes[0] << 16) + (temp_humid_bytes[1] << 8) + temp_humid_bytes[2]
    )
    is_negative = base_num & 0x800000
    temp_as_int = base_num & 0x7FFFFF
    temp_as_float = int(temp_as_int / 1000) / 10.0
    if is_negative:
        temp_as_float = -temp_as_float
    humid = (temp_as_int % 1000) / 10.0
    return temp_as_float, humid


def decode_temps_probes(packet_value: int) -> float:
    """Filter potential negative temperatures."""
    if packet_value < 0:
        return 0.0
    return float(packet_value / 100)


def decode_temps_probes_none(packet_value: int) -> float | None:
    """Filter potential negative temperatures."""
    if packet_value < 0:
        return None
    return float(packet_value)


def hex(data: bytes) -> str:
    """Return a string object containing two hexadecimal digits for each byte in the instance."""
    return "b'{}'".format("".join(f"\\x{b:02x}" for b in data))


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
        if debug_logging := _LOGGER.isEnabledFor(logging.DEBUG):
            _LOGGER.debug("Parsing Govee sensor: %s %s", mgr_id, hex(data))
        msg_length = len(data)
        if msg_length > 25 and b"INTELLI_ROCKS" in data:
            # INTELLI_ROCKS sometimes ends up glued on to the end of the message
            data = data[:-25]
            msg_length = len(data)
            if debug_logging:
                _LOGGER.debug("Cleaned up packet: %s %s", mgr_id, hex(data))

        if msg_length == 6 and (
            "H5072" in local_name or "H5075" in local_name or mgr_id == 0xEC88
        ):
            self.set_device_type("H5072/H5075")
            temp, humi = decode_temp_humid(data[1:4])
            batt = int(data[4] & 0x7F)
            err = bool(data[4] & 0x80)
            if temp >= MIN_TEMP and temp <= MAX_TEMP and not err:
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi)
            else:
                _LOGGER.debug(
                    "Ignoring invalid sensor values, temperature: %.1f, humidity: %.1f, error: %s",
                    temp,
                    humi,
                    err,
                )
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, ERROR)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, ERROR)
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
            return

        if msg_length in (6, 8) and (
            (is_5108 := "H5108" in local_name)
            or (is_5101 := "H5101" in local_name)
            or (is_5102 := "H5102" in local_name)
            or (is_5104 := "H5104" in local_name)
            or (is_5174 := "H5174" in local_name)
            or (is_5177 := "H5177" in local_name)
            or mgr_id == 0x0001
        ):
            if is_5108 or msg_length == 8:
                self.set_device_type("H5108")
            elif is_5101:
                self.set_device_type("H5101")
            elif is_5102:
                self.set_device_type("H5102")
            elif is_5104:
                self.set_device_type("H5104")
            elif is_5174:
                self.set_device_type("H5174")
            elif is_5177:
                self.set_device_type("H5177")
            else:
                self.set_device_type("H5101/H5102/H5108/H5177")
            temp, humi = decode_temp_humid(data[2:5])
            batt = int(data[5] & 0x7F)
            err = bool(data[5] & 0x80)
            if temp >= MIN_TEMP and temp <= MAX_TEMP and not err:
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi)
            else:
                _LOGGER.debug(
                    "Ignoring invalid sensor values, temperature: %.1f, humidity: %.1f, error: %s",
                    temp,
                    humi,
                    err,
                )
                self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, ERROR)
                self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, ERROR)
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

        if msg_length == 9 and (
            mgr_id == 0xEC88
            or "H5051" in local_name
            or "H5052" in local_name
            or "H5071" in local_name
        ):
            if "H5071" in local_name:
                self.set_device_type("H5071")
            elif "H5052" in local_name:
                self.set_device_type("H5052")
            else:
                self.set_device_type("H5051")
                self.set_device_name(f"H5051 {short_address(address)}")
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
            "H5178" in local_name or "B5178" in local_name or mgr_id == 0x0001
        ):
            temp, humi = decode_temp_humid(data[3:6])
            batt = int(data[6] & 0x7F)
            err = bool(data[6] & 0x80)
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
            elif debug_logging:
                _LOGGER.debug(
                    "Unknown sensor id for Govee H5178,"
                    " please report to the developers, data: %s",
                    hex(data),
                )
            if temp >= MIN_TEMP and temp <= MAX_TEMP and not err:
                self.update_predefined_sensor(
                    SensorLibrary.TEMPERATURE__CELSIUS, temp, device_id=device_id
                )
                self.update_predefined_sensor(
                    SensorLibrary.HUMIDITY__PERCENTAGE, humi, device_id=device_id
                )
            else:
                _LOGGER.debug(
                    "Ignoring invalid sensor values, temperature: %.1f, humidity: %.1f, error: %s",
                    temp,
                    humi,
                    err,
                )
                self.update_predefined_sensor(
                    SensorLibrary.TEMPERATURE__CELSIUS, ERROR, device_id=device_id
                )
                self.update_predefined_sensor(
                    SensorLibrary.HUMIDITY__PERCENTAGE, ERROR, device_id=device_id
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
            if not (ids := FOUR_PROBES_MAPPING.get(sensor_id)):
                if debug_logging:
                    _LOGGER.debug(
                        "Unknown sensor id: %s for a H5184, data: %s",
                        sensor_id,
                        hex(data),
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

        if msg_length == 20 and (
            "H5198" in local_name
            or mgr_id == 0x3022
            or "00009851-0000-1000-8000-00805f9b34fb" in service_uuids
        ):
            sensor_id = data[6]
            self.set_device_type("H5198")
            self.set_device_name(f"H5198 {short_address(address)}")
            (
                temp_probe_first,
                temp_alarm_first,
                low_temp_alarm_first,
                temp_probe_second,
                temp_alarm_second,
                low_temp_alarm_second,
            ) = PACKED_hhhhhh.unpack(data[8:20])
            if not (ids := FOUR_PROBES_MAPPING.get(sensor_id)):
                if debug_logging:
                    _LOGGER.debug(
                        "Unknown sensor id: %s for a H5198, data: %s",
                        sensor_id,
                        hex(data),
                    )
                return
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_first),
                decode_temps_probes(temp_alarm_first),
                ids[0],
                decode_temps_probes(low_temp_alarm_first),
            )
            self.update_temp_probe_with_alarm(
                decode_temps_probes(temp_probe_second),
                decode_temps_probes(temp_alarm_second),
                ids[1],
                decode_temps_probes(low_temp_alarm_second),
            )
            return

        if msg_length == 20 and "00005550-0000-1000-8000-00805f9b34fb" in service_uuids:
            self.set_device_type("H5055")
            self.set_device_name(f"H5055 {short_address(address)}")
            (
                temp_probe_first,
                temp_min_first,
                temp_max_first,
                _,
                temp_probe_second,
                temp_min_second,
                temp_max_second,
            ) = PACKED_hhhchhh_LITTLE.unpack(data[5:18])
            sensor_ids = data[3]
            if not (pids := SIX_PROBES_MAPPING.get(sensor_ids & 0xC0)):
                if debug_logging:
                    _LOGGER.debug(
                        "Unknown sensor id: %s for a H5055, data: %s",
                        sensor_ids,
                        hex(data),
                    )
                return
            if sensor_ids & pids[0][1]:
                self.update_temp_probe_with_alarm(
                    temp_probe_first,
                    decode_temps_probes_none(temp_max_first),
                    pids[0][0],
                    decode_temps_probes_none(temp_min_first),
                )
            if sensor_ids & pids[1][1]:
                self.update_temp_probe_with_alarm(
                    temp_probe_second,
                    decode_temps_probes_none(temp_max_second),
                    pids[1][0],
                    decode_temps_probes_none(temp_min_second),
                )
            batt = int(data[2] & 0x7F)
            self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
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
        self,
        temp: float,
        alarm_temp: float | None,
        probe_id: int,
        low_alarm_temp: float | None = None,
    ) -> None:
        """Update the temperature probe with the alarm temperature."""
        self.update_temp_probe(temp, probe_id)
        if alarm_temp is not None:
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS,
                alarm_temp,
                key=f"temperature_alarm_probe_{probe_id}",
                name=f"Temperature Alarm Probe {probe_id}",
            )
        if low_alarm_temp is not None:
            self.update_predefined_sensor(
                SensorLibrary.TEMPERATURE__CELSIUS,
                low_alarm_temp,
                key=f"low_temperature_alarm_probe_{probe_id}",
                name=f"Low Temperature Alarm Probe {probe_id}",
            )
