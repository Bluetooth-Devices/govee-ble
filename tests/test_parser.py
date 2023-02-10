import logging

from bluetooth_sensor_state_data import BluetoothServiceInfo, DeviceClass, SensorUpdate
from sensor_state_data import (
    DeviceKey,
    SensorDescription,
    SensorDeviceClass,
    SensorDeviceInfo,
    SensorValue,
    Units,
)

from govee_ble.parser import GoveeBluetoothDeviceData

GVH5051_SERVICE_INFO = BluetoothServiceInfo(
    name="",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={60552: b"\x00\xba\x0a\xf9\x0f\x63\x02\x01\x01"},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5075_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5075_2762",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={
        60552: b"\x00\x03A\xc2d\x00L\x00\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c"
    },
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5075_SERVICE_INFO_NEGATIVE_VALUES = BluetoothServiceInfo(
    name="GVH5075_2762",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={60552: b"\x00\xbc\x00\x04>'"},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5075_SERVICE_INFO_OVERSIZED_VALUES = BluetoothServiceInfo(
    name="GVH5075_2762",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={
        60552: b"\x00J\x00(;\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\xc2",
    },
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5075_SERVICE_INFO_OTHER_VALUES = BluetoothServiceInfo(
    name="GVH5075_2762",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={60552: b"\x00\x03\x0f\xc95\x00"},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5071_SERVICE_INFO = BluetoothServiceInfo(
    name="Govee_H5071_FD12",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={60552: b"\x00!\n\xb6\x12\x18\xc8\x00\x01"},
    service_uuids=[
        "0000180a-0000-1000-8000-00805f9b34fb",
        "0000fef5-0000-1000-8000-00805f9b34fb",
        "0000ec88-0000-1000-8000-00805f9b34fb",
    ],
    service_data={},
    source="local",
)
GVH5052_SERVICE_INFO = BluetoothServiceInfo(
    name="Govee_H5052_E81B",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={60552: b"\x00\x1c\x01\xa7\x14;\x00\x00\x02"},
    service_uuids=[
        "0000180a-0000-1000-8000-00805f9b34fb",
        "0000fef5-0000-1000-8000-00805f9b34fb",
        "0000ec88-0000-1000-8000-00805f9b34fb",
    ],
    service_data={},
    source="local",
)

GVH5177_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5177_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        1: b"\x01\x01\x036&dL\x00\x02\x15INTELLI_ROCKS_HWQw\xf2\xff\xc2"
    },
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5184_SERVICE_INFO_1 = BluetoothServiceInfo(
    name="GVH5184_XXXX",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        6966: b" \x01\x00\x01\x01\xe4\x01\x86\x0c\x1c\xff\xff\x86\n\xf0\xff\xff",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008451-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5184_SERVICE_INFO_2 = BluetoothServiceInfo(
    name="GVH5184_XXXX",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        6966: b" \x01\x00\x01\x01\xe4\x02\x86\x0b\xb8\xff\xff\x86\x0bT\xff\xff",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008451-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5198_SERVICE_INFO = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        12322: b"\x6c\x01\x00\x01\x01\xa4\xc2\x0f\x0e\x10\xff\xff\xff\xff\x08\xfc\xff\xff\xff\xff"
    },
    service_uuids=["00009851-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5198_VARIANT_SERVICE_INFO = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        12322: b"\x6c\x01\x00\x01\x01\xa3\xc1\x0f\x0b\xb8\xff\xff\xff\xff\t`\xff\xff\xff\xff"
    },
    service_uuids=["00009851-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5198_INVALID_SERVICE_INFO = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        12322: b"\x6c\x01\x00\x01\x01\xa3\xd4\x0f\x0b\xb8\xff\xff\xff\xff\t`\xff\xff\xff\xff"
    },
    service_uuids=["00009851-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5185_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5185_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        18994: b"\x87\x01\x00\x01\x01\xe4\xc1f\x084\xff\xff\xff\xff"
        b"\x084\xff\xff\xff\xffL\x00\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c"
    },
    service_uuids=["00008551-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5185_VARIANT_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5185_VAR2",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        818: b"T\x01\x00\x01\x01\xe4\xc1f\t\xc4\xff\xff\xff\xff\t\xc4\xff\xff\xff\xff",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008551-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)


GVH5185_VARIANT_2_SERVICE_INFO = BluetoothServiceInfo(
    name="Govee_H5185_4C17",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        19506: b"\x17\x01\x00\x01\x01\xd7\x01f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=[
        "00001800-0000-1000-8000-00805f9b34fb",
        "00001801-0000-1000-8000-00805f9b34fb",
        "02f00000-0000-0000-0000-00000000fe00",
        "494e5445-4c4c-495f-524f-434b535f4857",
    ],
    service_data={},
    source="local",
)

GVH5183_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5183_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        26589: b"\xef\x01\x00\x01\x01\xe4\x01\x80\x084\xff\xff\x00"
        b"\x00L\x00\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c"
    },
    service_uuids=["00008351-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5183_NO_LOCAL_NAME_SERVICE_INFO = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        57391: b"\xcb\x01\x00\x01\x01\xe4\x00\x8f\x084\xff\xff\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008351-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5183_SERVICE_INFO_VARIANT = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        63391: b"s\x01\x00\x01\x01\xe4\x00\x80\n\xf0\xff\xff\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008351-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5181_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5181_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        14474: b"\xd8\x01\x00\x01\x01\xe4\x01\x86\x08\x98\x1d"
        b"\x10\x00\x00L\x00\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c"
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5181_VARIANT_SERVICE_INFO = BluetoothServiceInfo(
    name="GVH5181_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        59970: b"\xba\x01\x00\x01\x01d\x00\x06\xff\xff\x1c\xe8\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5181_VARIANT_SERVICE_INFO_2 = BluetoothServiceInfo(
    name="GVH5181_2EC8",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        59970: b"\xba\x01\x00\x01\x01d\x00\x86\n(\x1c\xe8\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5181_VARIANT_SERVICE_INFO_3 = BluetoothServiceInfo(
    name="GVPROBE",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        63585: b"&\x01\x00\x01\x01\xe4\x01\x06\xff\xff\x1c\xd4\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5181_VARIANT_SERVICE_INFO_4 = BluetoothServiceInfo(
    name="",
    address="4125DDBA-2774-4851-9889-6AADDD4CAC3D",
    rssi=-56,
    manufacturer_data={
        43682: b"\xc1\x01\x00\x01\x01\xe4\x01\x86\x08\x98\x1a\xae\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5181_VARIANT_SERVICE_INFO_5 = BluetoothServiceInfo(
    name="",
    address="AA:BB:CC:DD:EE:FF",
    rssi=-56,
    manufacturer_data={
        53579: b"i\x01\x00\x01\x01\xe4\x01\x86\x07l \x1c\x00\x00",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c",
    },
    service_uuids=["00008151-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)

GVH5182_SERVICE_INFO = BluetoothServiceInfo(
    name="F34DC3CB-9CCF-336F-3CB1-3C6F525509E6",
    address="F34DC3CB-9CCF-336F-3CB1-3C6F525509E6",
    rssi=-56,
    manufacturer_data={
        10032: b"c\x01\x00\x01\x01\xe4\x01\x01\xff\xff\x12\x03\x01"
        b"\xff\xff\x00\x00L\x00\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\x0c"
    },
    service_uuids=["00008251-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
GVH5179_SERVICE_INFO = BluetoothServiceInfo(
    name="Govee_H5179_3CD5",
    address="10F1A254-16A5-9F35-BE40-7034507A6967",
    rssi=-50,
    manufacturer_data={34817: b"\xec\x00\x01\x01\n\n\xa4\x06d"},
    service_data={},
    service_uuids=[
        "0000180a-0000-1000-8000-00805f9b34fb",
        "0000fef5-0000-1000-8000-00805f9b34fb",
        "0000ec88-0000-1000-8000-00805f9b34fb",
    ],
    source="local",
)
GVH5074_SERVICE_INFO = BluetoothServiceInfo(
    name="Govee_H5074_5FF4",
    address="99214D75-854A-E52B-704D-C5C9B7F5D59C",
    rssi=-67,
    manufacturer_data={
        60552: b"\x00\xe6\t\xbc\x12d\x02",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\xc2",
    },
    service_data={},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    source="local",
)

GVH5178_SERVICE_INFO = BluetoothServiceInfo(
    name="B51782BC8",
    address="A4:C1:38:75:2B:C8",
    rssi=-66,
    manufacturer_data={
        1: b"\x01\x01\x01\x00\x2a\xf7\x64\x00\x03",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\xc2",
    },
    service_data={},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    source="local",
)
GVH5178_SERVICE_INFO_ERROR = BluetoothServiceInfo(
    name="B51782BC8",
    address="A4:C1:38:75:2B:C8",
    rssi=-66,
    manufacturer_data={
        1: b"\x01\x01\x01\x00\x03\xe7\xe4\x00\x01",
        76: b"\x02\x15INTELLI_ROCKS_HWPu\xf2\xff\xc2",
    },
    service_data={},
    service_uuids=["0000ec88-0000-1000-8000-00805f9b34fb"],
    source="local",
)


def test_can_create():
    GoveeBluetoothDeviceData()


def test_gvh5051():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5051_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5051 8105",
                model="H5051",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=27.46,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=40.89,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=99,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5052():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5052_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5052 E81B",
                model="H5052",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=2.84,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=52.87,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=59,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5071():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5071_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5071 FD12",
                model="H5071",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=25.93,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=47.9,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=24,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5075():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5075_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5075 2762",
                model="H5072/H5075",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=21.3,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=44.2,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5075_negative_values():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5075_SERVICE_INFO_NEGATIVE_VALUES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5075 2762",
                model="H5072/H5075",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value="error",
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value="error",
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=62,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5075_oversized_values():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5075_SERVICE_INFO_OVERSIZED_VALUES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5075 2762",
                model="H5072/H5075",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value="error",
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value="error",
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=59,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5075_other_values():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5075_SERVICE_INFO_OTHER_VALUES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5075 2762",
                model="H5072/H5075",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=20.0,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=64.9,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=53,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )


def test_gvh5177():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5177_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5177 2EC8",
                model="H5101/H5102/H5177",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=21.0,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=47.0,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5184_packet_type_1():
    parser = GoveeBluetoothDeviceData()
    result = parser.update(GVH5184_SERVICE_INFO_1)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5184 AC3D",
                model="H5184",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=31.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature Probe 2",
                native_value=28.0,
            ),
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature Alarm Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5184_packet_type_2():
    parser = GoveeBluetoothDeviceData()
    result = parser.update(GVH5184_SERVICE_INFO_2)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5184 AC3D",
                model="H5184",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_3", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_3", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_3", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_3", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_4", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_4", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_4", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_4", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_3", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_3", device_id=None),
                name="Temperature Probe 3",
                native_value=30.0,
            ),
            DeviceKey(key="temperature_alarm_probe_3", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_3", device_id=None),
                name="Temperature Alarm Probe 3",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_4", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_4", device_id=None),
                name="Temperature Probe 4",
                native_value=29.0,
            ),
            DeviceKey(key="temperature_alarm_probe_4", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_4", device_id=None),
                name="Temperature Alarm Probe 4",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5185():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5185_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5185 AC3D",
                model="H5185",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=21.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature Probe 2",
                native_value=21.0,
            ),
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature Alarm Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5185_variant():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5185_VARIANT_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5185 AC3D",
                model="H5185",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature " "Alarm " "Probe " "2",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=25.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature " "Probe " "2",
                native_value=25.0,
            ),
        },
    )


def test_gvh5185_2_variant():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5185_VARIANT_2_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5185 AC3D",
                model="H5185",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature " "Alarm " "Probe " "2",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature " "Probe " "2",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_gvh5183():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5183_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5183 AC3D",
                model="H5183",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=21.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5183_no_local_name():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5183_NO_LOCAL_NAME_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5183 AC3D",
                model="H5183",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=21.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5183_variant():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5183_SERVICE_INFO_VARIANT
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5183 AC3D",
                model="H5183",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=28.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=0.0,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_gvh5181():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 AC3D",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=22.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=74.4,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5181_variant():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_VARIANT_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 AC3D",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=74.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5181_variant_2():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_VARIANT_SERVICE_INFO_2
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 AC3D",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=26.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=74.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5181_variant_3():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_VARIANT_SERVICE_INFO_3
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 AC3D",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=73.8,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_gvh5181_variant_4():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_VARIANT_SERVICE_INFO_4
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 AC3D",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=22.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=68.3,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_gvh5181_variant_5():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5181_VARIANT_SERVICE_INFO_5
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5181 EEFF",
                model="H5181",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature " "Alarm " "Probe " "1",
                native_value=82.2,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-56,
            ),
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature " "Probe " "1",
                native_value=19.0,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_gvh5182():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5182_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5182 09E6",
                model="H5182",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=46.11,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature Alarm Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5179():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5179_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5179 3CD5",
                model="H5179",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=25.7,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=17.0,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-50,
            ),
        },
    )


def test_gvh5074():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5074_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5074 5FF4",
                model="H5074",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=25.34,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=47.96,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-67,
            ),
        },
    )


def test_gvh5178():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5178_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="B51782BC8",
        devices={
            None: SensorDeviceInfo(
                name=None,
                model=None,
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            ),
            "remote": SensorDeviceInfo(
                name="B51782BC8 Remote",
                model="H5178-REMOTE",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id="remote"),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id="remote"),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="battery", device_id="remote"),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id="remote"),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="temperature", device_id="remote"),
                name="Temperature",
                native_value=1.0,
            ),
            DeviceKey(key="humidity", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="humidity", device_id="remote"),
                name="Humidity",
                native_value=99.9,
            ),
            DeviceKey(key="battery", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="battery", device_id="remote"),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id="remote"),
                name="Signal Strength",
                native_value=-66,
            ),
        },
    )


def test_gvh5178_error():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5178_SERVICE_INFO_ERROR
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="B51782BC8",
        devices={
            None: SensorDeviceInfo(
                name=None,
                model=None,
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            ),
            "remote": SensorDeviceInfo(
                name="B51782BC8 Remote",
                model="H5178-REMOTE",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            ),
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id="remote"),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id="remote"),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="battery", device_id="remote"),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id="remote"): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id="remote"),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="temperature", device_id="remote"),
                name="Temperature",
                native_value="error",
            ),
            DeviceKey(key="humidity", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="humidity", device_id="remote"),
                name="Humidity",
                native_value="error",
            ),
            DeviceKey(key="battery", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="battery", device_id="remote"),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="signal_strength", device_id="remote"): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id="remote"),
                name="Signal Strength",
                native_value=-66,
            ),
        },
    )


def test_gvh5198_probe_1_2():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5198_VARIANT_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5198 AC3D",
                model="H5198",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="low_temperature_alarm_probe_1", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_1", device_id=None
                ),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="low_temperature_alarm_probe_2", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_2", device_id=None
                ),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_1", device_id=None),
                name="Temperature Probe 1",
                native_value=30.0,
            ),
            DeviceKey(key="temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_1", device_id=None),
                name="Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="low_temperature_alarm_probe_1", device_id=None): SensorValue(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_1", device_id=None
                ),
                name="Low Temperature Alarm Probe 1",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_2", device_id=None),
                name="Temperature Probe 2",
                native_value=24.0,
            ),
            DeviceKey(key="temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_2", device_id=None),
                name="Temperature Alarm Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="low_temperature_alarm_probe_2", device_id=None): SensorValue(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_2", device_id=None
                ),
                name="Low Temperature Alarm Probe 2",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5198_probe_3_4():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5198_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5198 AC3D",
                model="H5198",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature_probe_3", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_3", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_3", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_3", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="low_temperature_alarm_probe_3", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_3", device_id=None
                ),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="temperature_probe_4", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature_probe_4", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="temperature_alarm_probe_4", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(key="temperature_alarm_probe_4", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(
                key="low_temperature_alarm_probe_4", device_id=None
            ): SensorDescription(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_4", device_id=None
                ),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature_probe_3", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_3", device_id=None),
                name="Temperature Probe 3",
                native_value=36.0,
            ),
            DeviceKey(key="temperature_alarm_probe_3", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_3", device_id=None),
                name="Temperature Alarm Probe 3",
                native_value=0.0,
            ),
            DeviceKey(key="low_temperature_alarm_probe_3", device_id=None): SensorValue(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_3", device_id=None
                ),
                name="Low Temperature Alarm Probe 3",
                native_value=0.0,
            ),
            DeviceKey(key="temperature_probe_4", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_probe_4", device_id=None),
                name="Temperature Probe 4",
                native_value=23.0,
            ),
            DeviceKey(key="temperature_alarm_probe_4", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature_alarm_probe_4", device_id=None),
                name="Temperature Alarm Probe 4",
                native_value=0.0,
            ),
            DeviceKey(key="low_temperature_alarm_probe_4", device_id=None): SensorValue(
                device_key=DeviceKey(
                    key="low_temperature_alarm_probe_4", device_id=None
                ),
                name="Low Temperature Alarm Probe 4",
                native_value=0.0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5198_invalid():
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5198_INVALID_SERVICE_INFO
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5198 AC3D",
                model="H5198",
                manufacturer="Govee",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-56,
            ),
        },
    )


def test_gvh5075_debug_hex(caplog):
    parser = GoveeBluetoothDeviceData()
    service_info = GVH5075_SERVICE_INFO
    with caplog.at_level(logging.DEBUG):
        parser.update(service_info)
    assert (
        "Parsing Govee sensor: 60552 b'\\x00\\x03\\x41\\xc2\\x64\\x00\\x4c\\x00\\x02\\x15\\x49\\x4e\\x54"
        "\\x45\\x4c\\x4c\\x49\\x5f\\x52\\x4f\\x43\\x4b\\x53\\x5f\\x48\\x57\\x50\\x75\\xf2\\xff\\x0c'"
        in caplog.text
    )
