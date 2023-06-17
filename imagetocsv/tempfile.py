from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any


class TemporaryFile:
    def __init__(self, name: str, io: Any, delete: bool):
        self.name = name
        self.__io = io
        self.__delete = delete

    def __getattr__(self, k: Any) -> Any:
        return getattr(self.__io, k)

    def __del__(self) -> None:
        if self.__delete:
            try:
                os.unlink(self.name)
            except FileNotFoundError:
                pass


def NamedTemporaryFile(
    mode: str | None = "w+b",
    bufsize: int = -1,
    suffix: str = "",
    prefix: str = "tmp",
    dir: Path | str | None = None,
    delete: bool = True,
) -> TemporaryFile:
    if not dir:
        dir = tempfile.gettempdir()
    name = os.path.join(dir, prefix + os.urandom(32).hex() + suffix)
    if mode is None:
        return TemporaryFile(name, None, delete)
    fh = open(name, "w+b", bufsize)
    if mode != "w+b":
        fh.close()
        fh = open(name, mode)
    return TemporaryFile(name, fh, delete)
