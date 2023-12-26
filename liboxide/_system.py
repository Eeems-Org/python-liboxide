from ._base import API
from ._util import static_init


@static_init
class SystemAPI(API):
    properties = [
        "autoSleep",
        "sleepInhibited",
        "powerOffInhibited",
    ]
    methods = [
        ("suspend", None),
        ("powerOff", None),
        ("reboot", None),
        ("activity", None),
        ("inhibitSleep", None),
        ("uninhibitSleep", None),
        ("inhibitPowerOff", None),
        ("uninhibitPowerOff", None),
    ]
    signals = [
        ("leftAction",),
        ("homeAction",),
        ("rightAction",),
        ("powerAction",),
        ("sleepInhibitedChanged", bool),
        ("powerOffInhibitedChanged", bool),
        ("autoSleepChanged", bool),
        ("deviceSuspending",),
        ("deviceResuming",),
    ]
