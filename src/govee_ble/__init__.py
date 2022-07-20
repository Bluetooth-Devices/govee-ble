"""Parser for Govee BLE advertisements.

This file is shamlessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/govee.py

MIT License applies.
"""
from __future__ import annotations

from bluetooth_sensor_state_data import SIGNAL_STRENGTH_KEY
from sensor_state_data import DeviceClass, DeviceKey, SensorUpdate
from sensor_state_data.data import (
    ATTR_HW_VERSION,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME,
    ATTR_SW_VERSION,
    SensorDeviceInfo,
)

from .parser import GoveeBluetoothDeviceData

__version__ = "0.10.2"

__all__ = [
    "GoveeBluetoothDeviceData",
    "SIGNAL_STRENGTH_KEY",
    "ATTR_HW_VERSION",
    "ATTR_MANUFACTURER",
    "ATTR_MODEL",
    "ATTR_NAME",
    "ATTR_SW_VERSION",
    "SIGNAL_STRENGTH_KEY",
    "SensorDeviceInfo",
    "DeviceClass",
    "DeviceKey",
    "SensorUpdate",
    "SensorDeviceInfo",
]
