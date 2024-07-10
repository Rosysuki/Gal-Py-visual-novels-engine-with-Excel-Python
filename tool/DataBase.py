# -*- coding: utf-8 -*-


if "DataBase.py" in __file__:
    from tkinter.messagebox import showerror
    from typing import NoReturn ,Self ,NewType ,Any
    from csv import DictWriter ,DictReader
    from os import path
    from glob import glob ,iglob
    from pprint import pformat ,pp
    from re import findall as re_findall
    import pymysql as sql


class PyMySql(object):

    def __init__(self ,
                 db: str = "Gal_Py" ,
                 * ,
                 host: str = "localhost",
                 port: int = 3306 ,
                 password: str = "135790" ,
                 user: str = "root"
                 ) -> NoReturn:

        self.__connect: Any = sql.connect(
                    host = host ,
                    port = port ,
                    password = password ,
                    user = user ,
                    db = db
            )

        self.__cursor: Any = self.__connect.cursor()

    def exec(self ,command: str) -> Any:
        return self.__cursor.execute(command)

    def get(self) -> Any:
        ...
    

class CsvDataBase(object):

    @staticmethod
    def abspath(path: str ,target: str ,* ,mode: str = '') -> str|int:
        """
        可以优化！
        """
        #print(f"{path=}\n{target=}\n{mode=}")
        for index ,each in enumerate(iglob(path+f"{mode}\\*") ,start=1):
            if len(re_findall(r".*?({}).*?".format(target) ,target)):
                return each
        #showerror("错误" ,"未找到{}！".format(target))
        return 1
    

    def __init__(self ,
                 fmt_path: str = False ,
                 * ,
                 encoding: str = 'utf-8-sig'
                 ) -> NoReturn:
        
        self.encoding: str = encoding
        self.fmt_path: str = fmt_path

    def creater(self ,
                _path: str ,
                * ,
                default: str = r"__rule__.csv" ,
                path_: str = ''
                ) -> NoReturn:

        header: list[dict] = self.reader(default ,path_=path_)
        #pp(header)

        with open(_path ,'w' ,encoding=self.encoding ,newline='') as file:
            writer: DictWriter = DictWriter(file ,fieldnames=list(header[0]))
            writer.writeheader()
        
    

    def writer(self ,
               * ,
               data: list[dict[Ellipsis]] ,
               _path: str
               ) -> bool:
        
        if not all([isinstance(data ,list) ,*[isinstance(each ,dict) for each in data]]):
            showerror(title="数据格式错误！" ,message="数据格式应为:\nlist[dict[Any]]!")
            return False
    
     
        with open(_path ,'w' ,encoding=self.encoding ,newline='') as file:
            writer: DictWriter = DictWriter(file ,fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
        return True
    

    def reader(self ,_path: str ,* ,path_: str = 0) -> bool|list[dict]:
        if not path.exists(_path):
            showerror("路径不存在！" ,f"{_path}\n不存在！")
            return False
        
        with open(_path ,'r' ,encoding=self.encoding ,newline='') as file:
            reader: DictReader = DictReader(file)
            data: list[dict] = [each for index ,each in enumerate(reader)]

        set: dict = {"main":"pic" ,"song":"bgm" ,"back":"pic"}
        return data if not self.fmt_path else [{key : CsvDataBase.abspath(path_ ,each ,mode=set[key]) if key in set else each\
                                                for index ,(key ,each) in enumerate(e.items())} for i ,e in enumerate(data)]
    

    @staticmethod
    def gather(dir: str ,* ,mode: str = 'list') -> Any:
        if not path.exists(dir):
            showerror(title="路径不存在！" ,message=f"{dir}\n不存在！")
            return False
        
        return glob(dir) if mode=='list' else iglob(dir)


if __name__ == "__main__":
    database: CsvDataBase = CsvDataBase(r"‪C:\Users\sfuch\Desktop\Gal♥Py\data\momo")
    #data: Any = database.reader("__rule__.csv")
    #print(pformat(data))
    database.creater("OK.csv" ,path_=r"C:\Users\sfuch\Desktop\Gal♥Py\tool")
    
