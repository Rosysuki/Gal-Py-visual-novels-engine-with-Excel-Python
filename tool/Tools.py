# -*- coding: utf-8 -*-
#__all__: list = []

if "Tools.py" in __file__:
    from ctypes import *
    from typing import Any ,Self ,NoReturn ,Callable ,NewType
    from tkinter.messagebox import showerror
    from abc import ABC ,abstractmethod

ctype: NewType = NewType("ctype" ,Any)

class DLL(object):

    Memory: dict[Callable:bool] = {}

    dirpath: str = '//'.join(__file__.split('\\')[:-1]) + "//"

    def __init__(self ,dll: str) -> NoReturn:
        self.__dll: Any = WinDLL(dll)

    @property
    def function(self) -> Callable:
        return self.__dll

    def config(self ,
               target: Callable ,
               * ,
               res: ctype,
               args: list[ctype]
               ) -> bool:

        try:
            target.restype: ctype = res
            target.argtypes: list[ctype] = args
        except Exception as Error:
            showerror("错误" ,str(Error))
            return False
        return True


class StructureInC(ABC):

    PATH: str = DLL.dirpath+r"dll\x64\Debug\dll.dll"

    def __init__(self) -> NoReturn:
        self.__dll: DLL = DLL(PATH)


class SqStack(StructureInC):

    class __SqStack__(Structure):
        _fields_: tuple[tuple] = (
                    ("data" ,POINTER(c_int)) ,
                    ("top" ,c_int) ,
                    ("base" ,c_int)
                )

    def __init__(self ,MAXSIZE: int = 10) -> NoReturn:
        super(Stack ,self).__init__()
        array: SqStack = (c_int * MAXSIZE)()
        stack: SqStack = POINTER(c_int).from_buffer(array)
        self.__stack: SqStack = SqStack.__SqStack__(stack ,0 ,0)
        self.__SqStackInit: Callable = self.__dll.function.SqStackInit
        self.__SqStackPush: Callable = self.__dll.function.SqStackPush
        self.__SqStackPop: Callable = self.__dll.function.SqStackPop
        self.__dll.config(self.__SqStackInit ,res=c_int ,args=[POINTER(SqStack.__SqStack__) ,c_int])
        self.__dll.config(self.__SqStackPush ,res=c_int ,args=[POINTER(SqStack.__SqStack__) ,c_int])
        self.__dll.config(self.__SqStackPop ,res=c_int ,args=[POINTER(SqStack.__SqStack__) ,POINTER(c_int)])
        self.__SqStackInit(byref(self.__stack) ,MAXSIZE)

    def push(self ,value: int) -> int:
        return self.__SqStackPush(byref(self.__stack) ,c_int(value))

    def pop(self ,data: Any) -> int:
        return self.__SqStackPop(byref(self.__stack) ,byref(data))


class SqList(StructureInC):

    class __SqList__(Structure):
        _fields_: tuple[tuple] = (
                    ("data" ,POINTER(c_int)) ,
                    ("length" ,c_int)
                )

    def __init__(self ,MAXSIZE: int) -> NoReturn:
        super(SqList ,self).__init__()
        #array: SqStack = ()

if __name__ == "__main__":
    dll: DLL = DLL(DLL.dirpath+r"dll\x64\Debug\dll.dll")
    test: Callable = dll.function.test
    dll.config(test ,res=c_int ,args=[c_int ,c_int])
    pass

    








    
