import itertools
import json
import subprocess


class XDGSettingsException(Exception):
    pass


class Settings(object):
    @classmethod
    def get(cls, key, subkey=None):
        args = [key]
        if subkey is not None:
            args.append(subkey)

        stdout = subprocess.check_output(["/opt/bin/xdg-settings", "get"] + args)
        if stdout:
            return json.loads(stdout)

        return None

    @classmethod
    def set(cls, key: tuple[str] | str, val):
        if isinstance(key, str):
            args = [key]
        elif isinstance(key, tuple[str]):
            args = list(key)
        else:
            raise ValueError()

        args.append(val)
        stdout = subprocess.check_output(["/opt/bin/xdg-settings", "set"] + args)
        if stdout:
            return json.loads(stdout)

        return None

    @classmethod
    def keys(cls) -> tuple[str]:
        stdout = subprocess.check_output(["/opt/bin/xdg-settings", "--list"])
        lines = stdout.decode("utf-8").rstrip().split("\n")
        res = []
        if lines.pop(0) != "Known properties:":
            raise XDGSettingsException("Unknown xdg-settings output")

        peeker, lines = itertools.tee(lines)
        next(peeker)
        category = None
        for line in lines:
            key = line.lstrip().split(" ")[0]
            next_line = next(peeker, None)
            eof = next_line is None
            next_is_indented = not eof and next_line.startswith("    ")
            is_indented = line.startswith("    ")
            if category is not None and not is_indented:
                category = None

            if not is_indented and next_is_indented:
                category = key
                continue

            if category is None and not is_indented and (eof or not next_is_indented):
                res.append((key, None))
                continue

            if category is not None and is_indented:
                res.append((category, key))
                continue

            raise XDGSettingsException(
                "Unable to parse xdg-settings --list output\n"
                f"  Current line: {line}\n"
                f"  Line indented: {is_indented}\n"
                f"  Next line indented: {next_is_indented}\n"
                f"  Category: {category}"
            )

        return res

    @classmethod
    def items(cls):
        for key in cls.keys():
            yield (key, cls.get(*key))

    @classmethod
    def values(cls):
        for key in cls.keys():
            yield cls.get(*key)
