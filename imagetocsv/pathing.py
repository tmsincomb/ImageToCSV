"""
Home for string tools and any other misc tool until its large enough for it's own file
"""
from __future__ import annotations

import os
from pathlib import Path


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def pathing(path: str, new: bool = False, overwrite: bool = True) -> Path:
    """Guarantees correct expansion rules for pathing.
    :param Union[str, Path] path: path of folder or file you wish to expand.
    :param bool new: will check if distination exists if new  (will check parent path regardless).
    :return: A pathlib.Path object.
    >>> pathing('~/Desktop/folderofgoodstuffs/')
    /home/user/Desktop/folderofgoodstuffs
    """
    path = Path(path)
    # Expand shortened path
    if str(path)[0] == "~":
        path = path.expanduser()
    # Exand local path
    if str(path)[0] == ".":
        path = path.resolve()
    else:
        path = path.absolute()
    # Making sure new paths don't exist while also making sure existing paths actually exist.
    if new:
        if not path.parent.exists():
            raise ValueError(f"ERROR ::: Parent directory of {path} does not exist.")
        if path.exists() and not overwrite:
            raise ValueError(f"ERROR ::: {path} already exists!")
    else:
        if not path.exists():
            raise ValueError(f"ERROR ::: Path {path} does not exist.")
    return
