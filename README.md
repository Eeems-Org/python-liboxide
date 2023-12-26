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
```
