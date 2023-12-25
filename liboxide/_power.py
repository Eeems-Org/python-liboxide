from ._base import API
from ._util import static_init


@static_init
class PowerAPI(API):
    properties = [
        "state",
        "batteryState",
        "batteryLevel",
        "batteryTemperature",
        "chargerState",
    ]
