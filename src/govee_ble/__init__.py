"""Parser for Govee BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""

from __future__ import annotations

from sensor_state_data import (
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from .parser import GoveeBluetoothDeviceData, SensorType, get_model_info

__version__ = "0.35.1"

__all__ = [
    "GoveeBluetoothDeviceData",
    "SensorType",
    "SensorDescription",
    "SensorDeviceInfo",
    "DeviceClass",
    "DeviceKey",
    "SensorUpdate",
    "SensorDeviceInfo",
    "SensorValue",
    "Units",
    "get_model_info",
]
