# Installation

`govee-ble` is published on [PyPI](https://pypi.org/project/govee-ble/) and
requires **Python 3.10 or newer**.

## With pip

```bash
pip install govee-ble
```

## With Poetry

```bash
poetry add govee-ble
```

## Verifying the install

```python
import govee_ble
print(govee_ble.__version__)
```

Once installed, see [Usage](usage.md) for how to decode Govee BLE
advertisements into `SensorUpdate` objects.
