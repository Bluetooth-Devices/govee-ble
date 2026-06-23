"""Parser for Govee BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""

from __future__ import annotations

from sensor_state_data import (
    BinarySensorDeviceClass,
    BinarySensorValue,
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceClass,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from .parser import GoveeBluetoothDeviceData, ModelInfo, SensorType, get_model_info

__version__ = "1.4.0"

__all__ = [
    "GoveeBluetoothDeviceData",
    "BinarySensorDeviceClass",
    "SensorDeviceClass",
    "BinarySensorValue",
    "SensorType",
    "SensorDescription",
    "SensorDeviceInfo",
    "DeviceClass",
    "DeviceKey",
    "SensorUpdate",
    "SensorValue",
    "Units",
    "get_model_info",
    "ModelInfo",
]
