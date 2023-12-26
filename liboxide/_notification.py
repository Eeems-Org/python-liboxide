from ._base import API
from ._base import APIObject
from ._util import classproperty
from ._util import rot
from ._util import static_init
from ._apps import AppsAPI


class Notification(APIObject):
    api = "notification"
    properties = [
        "identifier",
        "application",
        "text",
        "icon",
    ]
    methods = [
        ("display", None),
        ("remove", None),
        ("click", None),
    ]
    signals = [
        ("changed", dict[str, str]),
        ("removed",),
        ("displayed",),
        ("clicked",),
    ]


@static_init
class NotificationAPI(API):
    properties = [
        "notifications",
        "allNotifications",
        "unownedNotifications",
    ]
    methods = [
        ("add", Notification, str, str, str, str),
        ("take", Notification, bool, str),
        ("get", Notification, str),
    ]
    signals = [
        ("notificationAdded", Notification),
        ("notificationRemoved", Notification),
        ("notificationChanged", Notification),
    ]

    @classproperty
    def notifications(cls):
        res = rot(*cls.rotArgs, "get", "notifications")
        if res is None:
            return []

        return [Notification(x) for x in res]

    @classproperty
    def allNotifications(cls):
        res = rot(*cls.rotArgs, "get", "allNotifications")
        if res is None:
            return []

        return [Notification(x) for x in res]

    @classproperty
    def unownedNotifications(cls):
        res = rot(*cls.rotArgs, "get", "unownedNotifications")
        if res is None:
            return []

        return [Notification(x) for x in res]
