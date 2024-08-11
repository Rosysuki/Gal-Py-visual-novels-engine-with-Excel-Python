# -*- coding: utf-8 -*-

__all__: list = [
    "GalPy" ,"AllKeyWords" ,"KeyWords" ,
    "Parser" ,"mainpath" ,"datapath" ,"staticpath"
    ]

if "Interpreter.py" in __file__:
    from re import findall as re_findall ,compile as re_compile
    from enum import Enum ,unique
    from typing import Any ,NoReturn ,Self ,NewType ,Callable
    from tkinter.messagebox import showerror
    from pprint import pp ,pformat
    from glob import iglob ,glob
    from os.path import basename ,dirname
    from os import mkdir ,path
    from base64 import b64encode ,b64decode
    from sys import stderr


KeyWord: NewType = NewType("KeyWord" ,type)
basepath: str = '//'.join(__file__.split('\\')[:-1])
mainpath: str = '//'.join(__file__.split('\\')[:-2])
module: str = "//module//"
suffix: str = r".Gal♥Py"
datapath: str = "//data//"
staticpath: str = "//GalPy//"

class GalPy(object):

    define: Any = re_compile(r"^\$\s?[Dd][Ee][Ff][Ii][Nn][Ee]\s+(\S+)\s+(.+)")
    rdefine: Any = re_compile(r"^\$\s?[Rr][Dd][Ee][Ff][Ii][Nn][Ee]\s+(.+)\s+[Ee][Nn][Dd]\s+(\S+)")
    include_all: Any = re_compile(r"^\$\s?[Ii][Nn][Cc][Ll][Uu][Dd][Ee]\s+(\*)\s*")
    include: Any = re_compile(r"^\$\s?[Ii][Nn][Cc][Ll][Uu][Dd][Ee]\s+(.+)")
    undefine: Any = re_compile(r"^\$\s?[Uu][Nn][Dd][Ee][Ff][Ii][Nn][Ee]\s+(\S+)\s*")
    register: Any = re_compile(r"^\$\s?[Rr][Ee][Gg][Ii][Ss][Tt][Ee][Rr](.*)")
    unregister: Any = re_compile(r"\$\s?[Uu][Nn][Rr][Ee][Gg][Ii][Ss][Tt][Ee][Rr](.*)")
    

    events: str = basepath + module + "events" + suffix
    colors: str = basepath + module + "colors" + suffix
    locals: str = basepath + module + "locals" + suffix
    chinese: str = basepath + module + "chinese" + suffix
    create: str = basepath + module + "create" + suffix
    embody: str = basepath + module + "embody" + suffix
    
    ALLMODULE: list[str] = [events ,colors ,locals ,chinese ,embody]

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
    def count_space(cls ,text: str) -> int:
        if not text:
            return 0b0
        for index ,each in enumerate(text ,start=0):
            if each != ' ':
                break
        return index


@unique
class AllKeyWords(Enum):

    say: Callable
    said: Callable
    pic: Callable

"""
class KeyWords(object):

    def __init__(self ,
                 path: str ,
                 * ,
                 mode: str = "//*.Gal♥Py"
                 ) -> NoReturn:

        self.__dict: dict[str : str] = {}
        for index ,each in enumerate(iglob(path+mode) ,start=1):
            
            try:
                with open(each ,'r' ,encoding='utf-8') as file:
                    self.__dict[basename(each)[:-3]]: str = file.read()
                    
            except Exception as Error:
                showerror("错误" ,f"{Error}")
                break

        else:
            #print("KeyWord Load OK!")
            pass


    @property
    def value(self) -> dict[str : str]:
        return self.__dict
"""

def KeyWords() -> dict[str : str]:
    return {
        "window" : "#AB01FF" ,"screen" : "#FF6DD3" ,
        "echo" : "#0BBFFF" ,
        "define" : "#00FF5E" , "rdefine" : "#00FF5E" , "undefine" : "#00FF5E" ,#"ifdefine" : "#00FF5E" ,"ifndefine" : "#00FF5E" ,
        "register" : "00FF5E" ,"unregister" : "00FF5E" ,
        "include" : "#FF9139" ,
        "from" : "#FA3A89" ,"import" : "#61FFDE" ,
        "PyScreen" : "#8D00FF" ,
        "let" : "#EB3324"
        }



class Parser(object):


    @staticmethod
    def legal(text: str) -> tuple[bool ,dict ,set]:
        __dict: dict = {}
        __list: list = [each for each in text.split('\n') if "#" not in each and each != '']
        __register: set = set()

        #print(__list)
        
        for i ,e in enumerate(__list ,start = 1):

            #print(f"{e=}")

            if (res := GalPy.register.findall(e)).__len__():
                __register.add(res[0].strip())
                continue

            if not re_findall(r"([Dd][Ee][Ff][Ii][Nn][Ee])" ,e):
                continue

            if len((res := re_findall(r"^\$\s?[Rr][Dd][Ee][Ff][Ii][Nn][Ee]\s+(.+)\s+[Ee][Nn][Dd]\s+(\S+)" ,e))):
                pass
            
            elif len(res := re_findall(r"^\$\s?[Dd][Ee][Ff][Ii][Nn][Ee]\s+(\S+)\s+(.+)" ,e)):
                pass

            else:
                showerror("语法错误" ,f"Error: Line{i}\ninclude仅支持define/rdefine/register宏！")
                return (False ,{} ,set())
            
            __dict[res[0][0]]: dict[str : str] = res[0][1]
        else:
            #print(f"legal = {__dict}")
            return (True ,__dict ,__register)


    def __init__(self ,
                 screen: Any = None ,
                 * ,
                 daemon: bool = False
                 ) -> NoReturn:

        #if daemon:
        #    with open(path ,'w' ,encoding='utf-8') as file:
        #        file.write(str(text))
        self.screen: Any = screen
        self.__suffix: str = r".Gal♥Py"
        self.daemon: bool = daemon
        pass


    def get(self ,text: str) -> NoReturn:
        self.__text: str = text
        self.__list: str = [each if each != '' else False for index ,each in enumerate(text.split('\n'))]

        #print(f"{self.__text=}\nself.__list=" ,end='')
        #pp(self.__list)
        return self


    def __lshift__(self ,name: str) -> bool:
        """
        犯了一个错误：
            遍历列表却改变了self.__list!
        """
        keys: Any = None
        _dir ,_base = dirname(name) ,basename(name)
        _name: str = _base[:_base.index('.')]

        __list: list = []
        __dict: dict = {}
        __include: set = set()
        __register: set = set()

        #Gal♥Py
        if self.daemon:
            with open(_dir+f"//daemon {_name}.dat" ,'w' ,encoding="utf-8") as fp:
                fp.write(str(pformat(self.__list)))

        for index ,each in enumerate(self.__list[:] ,start=0):
            
            if (res := GalPy.define.findall(str(each))).__len__():
                __dict[res[0][0]]: dict[str : str] = res[0][1]
                continue

            if (res := GalPy.rdefine.findall(str(each))).__len__():
                __dict[res[0][0]]: dict[str : str] = res[0][1]
                continue

            if (res := GalPy.include_all.findall(str(each))).__len__():
                __include |= set(GalPy.ALLMODULE)
                continue

            if (res := GalPy.include.findall(str(each))).__len__():
                __include.add(eval(res[0]))
                continue

            if (res := GalPy.register.findall(str(each))).__len__():
                __register.add(res[0].strip())
                continue

            if (res := GalPy.undefine.findall(str(each))).__len__():
                try:
                    __dict.pop(res[0].strip())
                except KeyError as KE:
                    stderr.write(f"{res[0]}不存在...\n")
                continue

            if (res := GalPy.unregister.findall(str(each))).__len__():
                __register.discard(res[0].strip())
                continue

                #del self.__list[index]
            #print(f"{res=}")

        #__include: set = {eval(each) for each in __include}
        #print(f"{__include=}")
        
        #include
        for index ,each in enumerate(__include ,start=1):
            #print(f"{each=}")
            with open(each ,'r' ,encoding="utf-8" ,newline='') as file:
                DECODE_TEXT: str = GalPy.decode(file.read())
                #print(f"{DECODE_TEXT=}")
                if (res := Parser.legal(DECODE_TEXT))[0]:
                    __dict |= res[1]
                    __register |= res[2]

        else:
            #pp(__dict)
            #print(f"{__register=}")
            pass

        for index ,each in enumerate(self.__list ,start=1):

            if each and re_findall(r"^from\s+(\*)\s+import\s+(\*)\s*" ,each).__len__():
                __list.append("from GalPy.screen import *")
                __list.append("from GalPy.tools import *")
                continue

            if each and "$" not in each:

                for i ,(key ,item) in enumerate(__dict.items() ,start=1):
                    each: str = each.replace(key ,item)

                #each: str = each.replace("echo" ,"print")#.replace("<" ,"(").replace(">" ,")")

                for j ,e in enumerate(__register ,start=1):
                    if (res := re_findall(r"(.*){}(.*)".format(e) ,each.strip())).__len__():
                        if each.strip().count(e) == 1:
                            each: str = ''.join([res[0][0] ,e ,"(" ,res[0][1].strip() ,")"])
                        else:
                            showerror("错误" ,"过于复杂!")
                            stderr.write("语句有歧义！\n")
                            return
                
                #if (res := re_findall(r"\s*print(.*)" ,each.strip())).__len__():
                #    each: str = ' ' * GalPy.count_space(each) + ''.join(["print(" ,res[0].strip() ,")"])

                #if (res := re_findall(r"(.+)\s*<-\s*(\S+)" ,each.strip())).__len__():
                #    each: str = ' ' * GalPy.count_space(each) + ''.join([res[0][1] ,'=' ,res[0][0]])

                #if (res := re_findall(r"\s*[Ll][Ee][Tt]\s+(\S+)\s+->\s(.+)\s*" ,each.strip())).__len__():
                #    each: str = ' ' * GalPy.count_space(each) + ''.join([res[0][0] ,' = ' ,res[0][1]])

                while (res := re_findall(r"\s*[Ll][Ee][Tt]\s+(\S+)\s+->\s(.+)\s*" ,each.strip())).__len__():
                    each: str = ' ' * GalPy.count_space(each) + ''.join([res[0][0] ,' = ' ,res[0][1]])

                #if (res := re_findall(r"\s*"))
                    
                __list.append(each)

                
            #__list.append(1)

        else:
            __text: str = '\n'.join(__list)
            #print(f"{__text=}\n__list=" ,end='')
            #pp(__list)

            __text.replace(r'\t' ,'')

            with open(_dir+f"//{_name}.py" ,'w' ,encoding='utf-8') as file:
                file.write(__text)


    def __rshift__(self) -> NoReturn:
        pass


    def RunScreenModule(self ,text: str) -> bool:
        #print("RunScreenModule!")
        return re_findall(r"#\s*(<GalPy!>)\s*" ,text.split('\n')[0]).__len__()
        



if __name__ == "__main__":
    #key: KeyWords = KeyWords("key")
    #print(key.value)
    parser = Parser()
    #print(parser.getWH("screen.width = 123\n\nscreen.height=321"))
    #parser.get("import this\nprint(1)\nstart\npause\n")
    print(parser.RunScreenModule("# <GalPy!>"))
    #parser << r"C:\Users\sfuch\Desktop\Gal♥Py\tool\t.Gal♥Py"

    #test: str = "1234567890"
    #test2: str = GalPy.encode(test)
    #print(GalPy.decode(test2))

    #print(parser.legal("#-*-utf-8-*-\n#-*-123-*-\n\n$define TEST 123"))

    #print(GalPy.u202a(r"‪C:\Users\sfuch\Desktop\pic\cute.png") == r"C:\Users\sfuch\Desktop\pic\cute.png")

    #print('//'.join(__file__.split('\\')[:-2]))

    print(GalPy.count_space("    space 12 3 4"))
    
