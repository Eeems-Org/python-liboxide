from ._base import API
from ._base import APIObject
from ._util import classproperty
from ._util import rot
from ._util import static_init


class Network(APIObject):
    api = "wifi"
    properties = [
        "enabled",
        "ssid",
        "bSSs",
        "password",
        "protocol",
        "properties",
    ]
    methods = [
        ("connect", None),
        ("remove", None),
    ]
    signals = [
        ("stateChanged", bool),
        ("propertiesChanged", dict[str, str]),
        ("connected",),
        ("disconnected",),
        ("removed",),
    ]

    @property
    def bSSs(self):
        res = rot(*self.rotArgs, "get", "bSSs")
        if res is None:
            return []

        return [BSS(x) for x in res]


class BSS(APIObject):
    api = "wifi"
    properties = [
        "bssid",
        "ssid",
        "privacy",
        "frequency",
        "network",
        "key_mgmt",
    ]
    methods = [
        ("connect", Network),
    ]
    signals = [
        ("removed",),
        ("propertiesChanged", dict[str, str]),
    ]

    @property
    def network(self):
        path = rot(*self.rotArgs, "get", "network")
        if path == "/":
            return None

        return Network(path)


@static_init
class WifiAPI(API):
    properties = [
        "state",
        "bSSs",
        "link",
        "rssi",
        "network",
        "networks",
        "scanning",
    ]
    methods = [
        ("enable", None),
        ("disable", None),
        ("addNetwork", Network, str, dict[str, object]),
        ("getNetwork", Network, dict[str, object]),
        ("getBSS", BSS, dict[str, object]),
        ("scan", None, bool),
        ("reconnect", None),
        ("reassociate", None),
        ("disconnect", None),
        ("flushBSSCache", None, int),
        ("addBlob", None, str, str),
        ("removeBlob", None, str),
        ("getBlob", str, str),
    ]
    signals = [
        ("stateChanged", int),
        ("linkChanged", int),
        ("networkAdded", Network),
        ("networkRemoved", Network),
        ("networkConnected", Network),
        ("disconnected",),
        ("bssFound", BSS),
        ("bssRemoved", BSS),
        ("scanningChanged", bool),
    ]

    @classproperty
    def bSSs(cls):
        res = rot(*cls.rotArgs, "get", "bSSs")
        if res is None:
            return []

        return [BSS(x) for x in res]

    @classproperty
    def network(cls):
        path = rot(*cls.rotArgs, "get", "network")
        if path == "/":
            return None

        return Network(path)

    @classproperty
    def networks(cls):
        res = rot(*cls.rotArgs, "get", "networks")
        if res is None:
            return []

        return [Network(x) for x in res]
