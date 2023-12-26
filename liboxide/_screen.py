from ._base import API
from ._base import APIObject
from ._util import classproperty
from ._util import rot
from ._util import static_init


class Screenshot(APIObject):
    api = "screen"
    properties = [
        "blob",
        "path",
    ]
    methods = [
        ("remove", None),
    ]
    signals = [
        ("modified",),
        ("removed",),
    ]


@static_init
class ScreenAPI(API):
    properties = [
        "screenshots",
    ]
    methods = [
        ("addScreenshot", Screenshot, str),
        ("drawFullScreenImage", Screenshot, str),
        ("screenshot", Screenshot),
    ]
    signals = [
        ("screenshotAdded", Screenshot),
        ("screenshotRemoved", Screenshot),
        ("screenshotModified", Screenshot),
    ]

    @classproperty
    def screenshots(cls):
        res = rot(*cls.rotArgs, "get", "screenshots")
        if res is None:
            return []

        return [Screenshot(x) for x in res]
