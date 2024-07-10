# -*- coding: utf-8 -*-

from typing import NoReturn
from os import chdir
from tool.TkWindow import main as run

def main(*args: tuple ,**kwargs: dict) -> NoReturn:
    chdir("tool")
    run()

if __name__ == "__main__":
    main()
