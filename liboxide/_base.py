from ._util import _registerProperty
from ._util import _registerMethod


class API:
    rotArgs = []
    properties = []
    methods = []

    @staticmethod
    def _raise(e):
        raise e

    @classmethod
    def static_init(cls):
        cls.rotArgs = [cls.__name__.lower()[:-3]]
        for name in cls.properties:
            _registerProperty(cls, name)

        for name, retType, *args in cls.methods:
            _registerMethod(cls, name, retType, *args)


class APIObject:
    api = None
    properties = []
    methods = []

    def __init__(self, path):
        if not path.startswith(f"/codes/eeems/oxide1/{self.api}"):
            raise ValueError()

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
