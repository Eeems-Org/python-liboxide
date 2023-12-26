from ._util import _listenMethod
from ._util import _registerMethod
from ._util import _registerProperty


class SignalHandler:
    def __init__(self, host):
        self.__host = host

    def __getattr__(self, name):
        for _name, *signature in self.__host.signals:
            if name == _name:
                return _listenMethod(self.__host, name, *signature)

        raise NotImplementedError(name)


class API:
    rotArgs = []
    properties = []
    methods = []
    signals = []

    @staticmethod
    def _raise(e):
        raise e

    @classmethod
    def static_init(cls):
        cls.on = SignalHandler(cls)
        cls.rotArgs = [cls.__name__.lower()[:-3]]
        for name in cls.properties:
            _registerProperty(cls, name)

        for name, retType, *args in cls.methods:
            _registerMethod(cls, name, retType, *args)


class APIObject:
    api = None
    folder = None
    properties = []
    methods = []
    signals = []

    def __init__(self, path):
        self.on = SignalHandler(self)
        if self.__class__.folder is None:
            self.__class__.folder = self.__class__.__name__.lower()

        if not path.startswith(f"/codes/eeems/oxide1/{self.folder}"):
            raise ValueError(f"Invalid path for {self.__class__.__name__}: {path}")

        self._path = path
        self.rotArgs = [
            "--object",
            f"{self.__class__.__name__}:{path[20:]}",
            self.api,
        ]
        for name in self.properties:
            _registerProperty(self, name)

        for name, retType, *args in self.methods:
            _registerMethod(self, name, retType, *args)
