import subprocess
import json
import sys

from ._errors import TooFewArguments
from ._errors import TooManyArguments
from ._errors import ObjectNotFound
from ._errors import RotException


def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)

    def __contains__(self, obj):
        return True


def rot(*args):
    try:
        stdout = subprocess.check_output(["/opt/bin/rot"] + list(args))
        if stdout:
            return json.loads(stdout)
    except subprocess.CalledProcessError as e:
        stdout = e.output.decode("utf-8")
        if "org.freedesktop.DBus.Error.UnknownObject" in stdout:
            raise ObjectNotFound(stdout) from e

        raise RotException(stdout) from e

    return None


def _registerProperty(obj, name):
    if name in obj.__dict__.keys():
        return

    def fn(self):
        return rot(*self.rotArgs, "get", name)

    if type == type(obj):
        setattr(obj, name, classproperty(fn))
    else:
        setattr(obj.__class__, name, property(fn))


def _convert(_type, val):
    if _type is None:
        return None

    from ._base import APIObject

    if issubclass(_type, APIObject):
        return _type(val)

    if _type in (str, bool, int):
        return val

    raise NotImplementedError(_type)


def _createMethod(cls, name, retType, *signature):
    def fn(cls, *args):
        if len(args) > len(signature):
            raise TooManyArguments()

        if len(args) < len(signature):
            raise TooFewArguments()

        arguments = []
        for i in range(0, len(signature)):
            if not isinstance(args[i], signature[i]):
                raise TypeError()

            argType = signature[i]

            if argType == str:
                qtype = "QString"
            elif argType == int:
                qtype = "int"
            elif argType == bool:
                qtype = "bool"
            elif issubclass(argType, dict):
                qtype = "QVariant"
            else:
                raise NotImplementedError(argType)

            arguments.append(f"{qtype}:{json.dumps(args[0])}")

        return _convert(retType, rot(*cls.rotArgs, "call", name, *arguments))

    return fn


def _registerMethod(obj, name, retType, *signature):
    if name in obj.__dict__.keys():
        return

    if type == type(obj):
        setattr(
            obj,
            name,
            classmethod(_createMethod(obj, name, retType, *signature)),
        )
    else:
        setattr(
            obj,
            name,
            _createMethod(obj, name, retType, *signature),
        )


def _listenMethod(obj, name, *signature):
    if len(signature) > 1:
        raise NotImplementedError()

    # TODO cache these instead of creating them every time
    def fn():
        res = rot(*obj.rotArgs, "--once", "listen", name)
        if signature:
            return _convert(signature[0], res)

        return res

    return fn
