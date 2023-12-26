[![liboxide on PyPI](https://img.shields.io/pypi/v/liboxide)](https://pypi.org/project/liboxide)

Python wrapper around the oxide command line tools
==================================================

Installation
============

```bash
pip install liboxide
```

Usage
=====

```python
import liboxide

liboxide.wifi.enable()

print("Applications:")
for name, app in liboxide.apps.applications.items():
    print(f"  {name}: {app.bin}")

autoLock = liboxide.settings.get("autoLock")
print("Automatically locking after {autoLock} minutes")

print(f"Battery level: {liboxide.power.batteryLevel}")
while True:
    batteryLevel = liboxide.power.on.batteryLevelChanged()
    print(f"Battery level: {batteryLevel}")
```
