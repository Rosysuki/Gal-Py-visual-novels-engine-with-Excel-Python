from base64 import b64encode ,b64decode
from typing import NoReturn ,Self ,Any ,Deque ,Callable
from os import system ,mkdir ,path ,getcwd ,chdir
from sys import path as sys_path
from collections import deque
from glob import iglob ,glob
from tkinter.messagebox import showerror
from re import findall as re_findall
from json import load as json_load ,dump as json_dump
from time import time ,strftime ,sleep

class GalPy(object):

    @classmethod
    def encode(cls ,text: str|bytes) -> str:
        return b64encode(text.encode("utf-8") if not isinstance(text ,bytes) else text).decode("utf-8")

    @classmethod
    def decode(cls ,text: str|bytes) -> str:
        return b64decode(text.encode('utf-8') if isinstance(text ,str) else text).decode('utf-8')

    @classmethod
    def u202a(cls ,text: str) -> str:
        return ''.join(list(text)[1:])

    @classmethod
    def io(cls ,
           path: str ,
           * ,
           text: str = '' ,
           suffix: str = ".txt" ,
           mode: str = "o" ,
           encoding: str = "utf-8"
           ) -> NoReturn:

        if mode not in {"i" ,"o"}:
            showerror("错误" ,"请正确使用参数！")
            return
        
        with open(path+suffix ,"r" if (io := mode.__eq__("o")) else "w" ,encoding=encoding) as file:
            if io:
                return file.read()
            file.write(text)
            

def color(vivid: str) -> tuple[int ,int ,int]:
    match vivid:
        case "red": lovely: str = (255 ,0 ,0)
        case "yellow": lovely: str = (255 ,255 ,0)
        case "blue": lovely: str = (0 ,0 ,255)
        case "green": lovely: str = (0 ,255 ,0)
        case "black": lovely: str = (0 ,0 ,0)
        case "white": lovely: str = (255 ,255 ,255)
        case "purple": lovely: str = (255 ,0 ,255)
        case "daisy": lovely: str = (255 ,128 ,0)
        case "violet": lovely: str = (138 ,43 ,226)
        case "pink": lovely: str = (255 ,89 ,236)
        case _: lovely: str = (255 ,255 ,255)
    return lovely
