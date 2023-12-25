from ._base import API
from ._base import APIObject
from ._util import classproperty
from ._util import rot
from ._util import static_init


class Application(APIObject):
    api = "apps"
    folder = "apps"
    properties = [
        "name",
        "processId",
        "permissions",
        "displayName",
        "description",
        "bin",
        "onPause",
        "onResume",
        "onStop",
        "autoStart",
        "type",
        "state",
        "systemApp",
        "hidden",
        "icon",
        "environment",
        "workingDirectory",
        "chroot",
        "user",
        "group",
        "directories",
    ]
    methods = [
        ("launch", None),
        ("pause", None),
        ("resume", None),
        ("stop", None),
        ("unregister", None),
        ("setEnvironment", None, dict[str, object]),
    ]


@static_init
class AppsAPI(API):
    properties = [
        "startupApplication",
        "lockscreenApplication",
        "applications",
        "previousApplications",
        "currentApplications",
        "runningApplications",
        "pausedApplications",
    ]
    methods = [
        ("openDefaultApplication", None),
        ("openTaskManager", None),
        ("openLockScreen", None),
        ("registerApplication", None, dict[str, object]),
        ("unregisterApplication", Application, str),
        ("reload", None),
        ("getApplicationPath", str, str),
        ("previousApplication", Application),
    ]

    @classmethod
    def getApplication(cls, name):
        return Application(cls.getApplicationPath(name))

    @classproperty
    def applications(cls):
        res = rot(*cls.rotArgs, "get", "applications")
        if res is None:
            return {}

        for name, path in res.items():
            res[name] = Application(path)

        return res
