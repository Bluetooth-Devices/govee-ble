"""
Parser for Govee BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""

from __future__ import annotations

import logging
import struct
from dataclasses import dataclass
from enum import Enum

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import BinarySensorDeviceClass, SensorLibrary

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_LOGGER = logging.getLogger(__name__)


PACKED_hHB_LITTLE = struct.Struct("<hHB")
PACKED_hHB = struct.Struct(">hHB")
PACKED_hh = struct.Struct(">hh")
PACKED_hhhchhh_LITTLE = struct.Struct("<hhhchhh")

PACKED_hhbhh = struct.Struct(">hhbhh")
PACKED_hhhhh = struct.Struct(">hhhhh")
PACKED_hhhhhh = struct.Struct(">hhhhhh")


ERROR = "error"

MIN_TEMP = -40
MAX_TEMP = 100

NOT_GOVEE_MANUFACTURER = {76}

PROBE_MAPPING_1_2 = [1, 2]
PROBE_MAPPING_3_4 = [3, 4]

FOUR_PROBES_MAPPING = dict.fromkeys(
    (1, 65, 129, 193), PROBE_MAPPING_1_2
) | dict.fromkeys((2, 66, 130, 194), PROBE_MAPPING_3_4)

SIX_PROBES_MAPPING = {
    0: [[1, 0x01], [2, 0x02]],
    64: [[3, 0x04], [4, 0x08]],
    128: [[5, 0x10], [6, 0x20]],
}


def decode_temp_humid_battery_error(data: bytes) -> tuple[float, float, int, bool]:
    temp, humi = decode_temp_humid(data[0:3])
    batt = int(data[-1] & 0x7F)
    err = bool(data[-1] & 0x80)
    return temp, humi, batt, err


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


def decode_temps_from_4_bytes(packet_value: int) -> float:
    """Decode temperature values (to one decimal place)."""
    if packet_value & 0x80000000:
        # Handle freezing temperatures
        packet_value &= 0x7FFFFFFF
        return float(int(packet_value / -10000000) / -10)
    return float(int(packet_value / 1000000) / 10)


def decode_humi_from_4_bytes(packet_value: int) -> float:
    """Decode humidity values (to one decimal place)"""
    packet_value &= 0x7FFFFFFF
    return float(int((packet_value % 1000000) / 1000) / 10)


def decode_pm25_from_4_bytes(packet_value: int) -> int:
    """Decode humidity values"""
    packet_value &= 0x7FFFFFFF
    return int(packet_value % 1000)


def calculate_crc(data: bytes) -> int:
    crc = 0x1D0F
    for b in data:
        for s in range(7, -1, -1):
            mask = 0
            if (crc >> 15) ^ (b >> s) & 1:
                mask = 0x1021
            crc = ((crc << 1) ^ mask) & 0xFFFF
    return crc


def decrypt_data(key: bytes, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key[::-1]), modes.ECB())
    decryptor = cipher.decryptor()
    return (decryptor.update(data[::-1]) + decryptor.finalize())[::-1]


class SensorType(Enum):
    THERMOMETER = "thermometer"
    BUTTON = "button"
    MOTION = "motion"
    WINDOW = "window"
    VIBRATION = "vibration"
    PRESENCE = "presence"
    PRESSURE = "pressure"


@dataclass
class ModelInfo:
    """Model information for Govee sensors."""

    model_id: str
    sensor_type: SensorType
    button_count: int
    sleepy: bool


_MODEL_DB = {
    "H5121": ModelInfo("H5121", SensorType.MOTION, 0, True),
    "H5122": ModelInfo("H5122", SensorType.BUTTON, 1, True),
    "H5123": ModelInfo("H5123", SensorType.WINDOW, 0, True),
    "H5124": ModelInfo("H5124", SensorType.VIBRATION, 0, True),
    "H5125": ModelInfo("H5125", SensorType.BUTTON, 6, True),
    "H5126": ModelInfo("H5126", SensorType.BUTTON, 2, True),
    "H5127": ModelInfo("H5127", SensorType.PRESENCE, 0, True),
    "H5130": ModelInfo("H5130", SensorType.PRESSURE, 1, True),
}


def get_model_info(model_id: str) -> ModelInfo:
    """Get model information for a Govee sensor."""
    return _MODEL_DB.get(
        model_id, ModelInfo(model_id, SensorType.THERMOMETER, 0, False)
    )


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

    @property
    def device_type(self) -> str | None:
        """Return the device type."""
        primary_device_id = self.primary_device_id
        if device_type := self._device_id_to_type.get(primary_device_id):
            return device_type.partition("-")[0]
        return None

    @property
    def button_count(self) -> int:
        """Return the number of buttons on the device."""
        device_type = self.device_type
        assert device_type is not None
        return get_model_info(device_type).button_count

    @property
    def sensor_type(self) -> SensorType:
        """Return the sensor type."""
        device_type = self.device_type
        assert device_type is not None
        return get_model_info(device_type).sensor_type

    @property
    def sleepy(self) -> bool:
        """Return if the device is sleep."""
        device_type = self.device_type
        assert device_type is not None
        return get_model_info(device_type).sleepy

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
                _LOGGER.debug("Cleaned up packet: %s %s", mgr_id, data.hex())

        if msg_length == 24:
            time_ms = data[2:6]
            enc_data = data[6:22]
            enc_crc = data[22:24]
            if not calculate_crc(enc_data) == int.from_bytes(enc_crc, "big"):
                _LOGGER.debug("CRC check failed for H512/3x: %s", hex(data))
                return

            key = time_ms + bytes(12)
            try:
                decrypted = decrypt_data(key, enc_data)
            except ValueError:
                _LOGGER.warning("Failed to decrypt H512/3x: %s", hex(data))
                return
            _LOGGER.debug("Decrypted H512/3x: %s - %s", decrypted, decrypted.hex())
            model_id = decrypted[2]
            # GV5121
            # 01040302640100000000000000000000

            # GV5122
            # 01050802640000000000000000000000
            # 01050802640000000000000000000000

            # GV5123
            # 01050202640200000000000000000000

            # GV5124
            # 01030902640100000000000000000000

            # GV5125
            # 01010a02640000000000000000000000

            # GV5126
            # 01010b02640100000000000000000000

            # GV5130
            # 010e0d02640000000000000000000000
            sensor_type = SensorType.BUTTON
            if "GV5121" in local_name or model_id == 3:
                self.set_device_type("H5121")
                self.set_device_name(f"5121{short_address(address)}")
                sensor_type = SensorType.MOTION
            elif "GV5122" in local_name or model_id == 8:
                self.set_device_type("H5122")
                self.set_device_name(f"5122{short_address(address)}")
            elif "GV5123" in local_name or model_id == 2:
                self.set_device_type("H5123")
                self.set_device_name(f"5123{short_address(address)}")
                sensor_type = SensorType.WINDOW
            elif "GV5124" in local_name or model_id == 9:
                self.set_device_type("H5124")
                self.set_device_name(f"5124{short_address(address)}")
                sensor_type = SensorType.VIBRATION
            elif "GV5125" in local_name or model_id == 10:
                self.set_device_type("H5125")
                self.set_device_name(f"5125{short_address(address)}")
            elif "GV5126" in local_name or model_id == 11:
                self.set_device_type("H5126")
                self.set_device_name(f"5126{short_address(address)}")
            elif "GV5130" in local_name or model_id == 13:
                self.set_device_type("H5130")
                self.set_device_name(f"5130{short_address(address)}")
                sensor_type = SensorType.PRESSURE
            else:
                return

            battery_percentage = decrypted[4]
            button_number_pressed = decrypted[5]
            self.update_predefined_sensor(
                SensorLibrary.BATTERY__PERCENTAGE, battery_percentage
            )
            if sensor_type is SensorType.WINDOW:
                # H5123 is a door/window sensor
                self.update_predefined_binary_sensor(
                    BinarySensorDeviceClass.WINDOW, button_number_pressed == 2
                )
            elif sensor_type is SensorType.VIBRATION:
                # H5124 is a vibration sensor
                if button_number_pressed == 1:
                    self.fire_event("vibration", "vibration")
            elif sensor_type is SensorType.MOTION:
                if button_number_pressed == 1:
                    self.fire_event("motion", "motion")
            elif sensor_type is SensorType.PRESSURE:
                # H5130 is a pressure sensor
                if button_number_pressed == 16:
                    self.fire_event("button_0", "press")
                else:
                    self.update_predefined_binary_sensor(
                        BinarySensorDeviceClass.PRESENCE, button_number_pressed == 1
                    )
            else:
                self.fire_event(f"button_{button_number_pressed}", "press")
            return

        if msg_length == 6 and (
            (data.startswith(b"\xec\x00\x01\x01") and "H5127" in local_name)
            or mgr_id == 0x8803
        ):
            self.set_device_type("H5127")
            self.set_device_name(f"H5127{short_address(address)}")
            present = data[4] == 1
            motion = data[5] == 17
            self.update_predefined_binary_sensor(
                BinarySensorDeviceClass.OCCUPANCY, present
            )
            self.update_predefined_binary_sensor(BinarySensorDeviceClass.MOTION, motion)

        if msg_length == 6 and (
            (is_5072 := "H5072" in local_name)
            or (is_5075 := "H5075" in local_name)
            or mgr_id == 0xEC88
        ):
            if is_5072:
                self.set_device_type("H5072")
            elif is_5075:
                self.set_device_type("H5075")
            else:
                self.set_device_type("H5072/H5075")
            temp, humi, batt, err = decode_temp_humid_battery_error(data[1:5])
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
            or (is_5100 := "H5100" in local_name)
            or (is_5101 := "H5101" in local_name)
            or (is_5102 := "H5102" in local_name)
            or (is_5103 := "H5103" in local_name)
            or (is_5104 := "H5104" in local_name)
            or (is_5105 := "H5105" in local_name)
            or (is_5174 := "H5174" in local_name)
            or (is_5177 := "H5177" in local_name)
            or (is_5110 := "H5110" in local_name)
            or (is_5179 := "GV5179" in local_name)
            or (mgr_id == 0x0001 and msg_length == 8)
        ):
            if is_5108 or msg_length == 8:
                self.set_device_type("H5108")
            elif is_5100:
                self.set_device_type("H5100")
            elif is_5101:
                self.set_device_type("H5101")
            elif is_5102:
                self.set_device_type("H5102")
            elif is_5103:
                self.set_device_type("H5103")
            elif is_5104:
                self.set_device_type("H5104")
            elif is_5105:
                self.set_device_type("H5105")
            elif is_5174:
                self.set_device_type("H5174")
            elif is_5177:
                self.set_device_type("H5177")
            elif is_5110:
                self.set_device_type("H5110")
            elif is_5179:
                self.set_device_type("GV5179")
            else:
                self.set_device_type("H5101/H5102/H5104/H5108/H5174/H5177/GV5179")
            temp, humi, batt, err = decode_temp_humid_battery_error(data[2:6])
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
            temp, humi, batt, err = decode_temp_humid_battery_error(data[3:7])
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

        if msg_length == 6 and "H5106" in local_name:
            self.set_device_type("H5106")
            self.set_device_name(f"H5106 {short_address(address)}")
            packet_5106 = data[2:6].hex()
            four_bytes = int(packet_5106, 16)
            temp = decode_temps_from_4_bytes(four_bytes)
            humi = decode_humi_from_4_bytes(four_bytes)
            pm25 = decode_pm25_from_4_bytes(four_bytes)
            self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp)
            self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi)
            self.update_predefined_sensor(
                SensorLibrary.PM25__CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, pm25
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
