# -*- coding: utf-8 -*-

__VERSION__: str = "2.0"

__all__: list = ["TkWindow" ,"__VERSION__"]

if "TkWindow.py" in __file__:
    from tkinter import *
    from tkinter import ttk
    from tkinter.messagebox import showerror ,showinfo
    from tkinter import filedialog
    from tkinter.colorchooser import *
    from typing import NoReturn ,Self ,Any ,Deque ,Callable
    from os import system ,mkdir ,path ,getcwd ,chdir
    from sys import path as sys_path
    from collections import deque
    from glob import iglob ,glob
    from re import findall as re_findall
    from threading import Thread
    #from multiprocessing import Process
    from json import load as json_load ,dump as json_dump
    from time import time ,strftime ,sleep
    import asyncio
    
    from tool.PyScreen import *
    from tool.DataBase import CsvDataBase
    from tool.Interpreter import *
    

def test() -> NoReturn: showinfo("☺" ,"敬请期待！")

def update() -> NoReturn: showinfo("☺" ,"正在维护！")


class TkMeta(type):

    __MySelf__: Any = NotImplemented

    with open(r"tool//Hint.dat" ,'r' ,encoding="utf-8") as file:
        Hint: str = file.read()

    with open(r"tool//About.dat" ,'r' ,encoding="utf-8") as file:
        About: str = file.read()

    def __new__(mcls ,name: str ,bases: tuple ,attrs: dict) -> Any:
        if mcls.__MySelf__ is NotImplemented:
            attrs["info"]: dict = {"dir":None ,"AutoResolution":None ,"name":None ,"Version":__VERSION__ ,"width":0b0 ,"height":0b0}
            attrs["basepath"]: dict[str:str] = '//'.join(__file__.split('\\')[:-2])
            mcls.__MySelf__: Any = type.__new__(mcls ,name ,bases ,attrs)
        return mcls.__MySelf__

    def __call__(cls ,
                 path: str = '' ,
                 * ,
                 name: str = "TkWindow" ,
                 size: str = '1000x800' ,
                 pos: str = '100+50' ,
                 resize: tuple[bool ,bool] = (True ,True) ,
                 savepath: str = "//data//"
                 ) -> NoReturn:

        ...
        return type.__call__(cls ,path ,name=name ,size=size ,pos=pos ,resize=resize ,savepath=savepath)


class TopRoot(Toplevel):
    
    
    def __init__(self ,
                 * ,
                 name: str = "toproot" ,
                 size: str = '350x300' ,
                 pos: str = '200+150' ,
                 resize: tuple[bool ,bool] = (True ,True)
                 ) -> NoReturn:
        
        super(TopRoot ,self).__init__()
        self.title(name)
        self.geometry('+'.join([size ,pos]))
        self.resizable(width=resize[0] ,height=resize[1])
        self.NameVar: StringVar = StringVar()


    def prompt(self) -> NoReturn:
        prompt_var: Entry = ttk.Entry(self ,textvariable=self.NameVar)
        prompt_btn: Button = ttk.Button(self ,text="OK" ,command=self.get_name)
        prompt_var.pack()
        prompt_btn.pack()
        self.mainloop()
        return self.name


    def text(self ,target: str = '') -> NoReturn:
        self.x_bar ,self.y_bar = Scrollbar(self ,orient=HORIZONTAL) ,Scrollbar(self ,orient=VERTICAL)
        self.Text: Text = Text(self ,xscrollcommand=self.x_bar.set ,yscrollcommand=self.y_bar.set ,width=170 ,height=44)
        self.Text.config(font=("幼圆" ,15))
        self.Text.insert("1.0" ,target)
        self.Text.pack()



class TkWindow(Tk ,metaclass = TkMeta):


    File: dict[str : Menu] = {}
    Menu: Deque[Menu] = deque([])
    Memory: dict[str : bool] = {}


    def __lshift__(self ,PyScreen: Any) -> Self:
        """
        Ellipsis
        """
        self.screen: Any = PyScreen
        self.screen.database: CsvDataBase = self.database
        self.parser: Parser = Parser(self.screen ,daemon=True)
        return self


    def screen_run(self) -> NoReturn:
        if not self.__dict__.get("screen" ,False):
            delattr(self ,"screen")
            showerror("错误" ,"屏幕尚未初始化！")
            return

        if not self.name:
            showerror("错误" ,"没有数据！")
            return

        path_: str = ''.join([TkWindow.basepath ,self.savepath ,self.name ,'\\'])

        self.database.fmt_path: str = ''.join([TkWindow.basepath ,self.savepath ,f"{self.name}//{self.name}.csv"])

        (self.screen << self.database.reader(self.database.fmt_path ,path_=path_)).action()

        self.screen.reinit()


    def __repr__(self) -> repr:
        return "<class 'TkWindow'>"
    

    def __init__(self ,
                 path: str = '' ,
                 * ,
                 name: str = "TkWindow" ,
                 size: str = '1000x800' ,
                 pos: str = '100+50' ,
                 resize: tuple[bool ,bool] = (True ,True) ,
                 savepath: str = "//data//"
                 ) -> NoReturn:

        super(TkWindow ,self).__init__()
        self.title(name)
        self.geometry('+'.join([size ,pos]))
        self.resizable(width=resize[0] ,height=resize[1])
        self.width ,self.height = [int(each) for index ,each in enumerate(size.split('x'))]
        self.__suffix: str = ".Gal♥Py"
        
        self.NameVar: StringVar = StringVar()
        self.FileVar: StringVar = StringVar()
        
        self.x_bar ,self.y_bar = Scrollbar(self ,orient=HORIZONTAL) ,Scrollbar(self ,orient=VERTICAL)
        self.Text: Text = Text(self ,xscrollcommand=self.x_bar.set ,yscrollcommand=self.y_bar.set ,width=170 ,height=44)
        self.Text.config(font=("幼圆" ,13))
        self.Text.bind("<Tab>" ,lambda event : self.AutoSpace())
        
        self.name: str = None
        self.path: str = None
        self.pointer: int = 0b0
        self.path ,self.savepath = path ,savepath

        self.AutoResolution: bool = None
        self.AutoTagAdd: Any = Thread(name="TagAdd" ,target=self.TagAdd)
        self.AutoTagAddBtn: bool = False
        self.KeyWords: dict[str : str] = KeyWords()

        self.TempList: list = []
        
        self.target_file: str = None
        #self.target_file_label: Label = ttk.Label()

        self.database: CsvDataBase = CsvDataBase(False)

        TemplatePath: str = TkWindow.basepath+"//tool//template//{}.py"
        self.Template: dict[int : str] = {
                                            1 : TemplatePath.format("mainloop") ,
                                            2 : TemplatePath.format("init") ,
                                            0 : TemplatePath.format("all")
                                         }

        if not self.__isTemplateExists:
            return


    def start(self) -> NoReturn:
        """
        //menu0 -> 运行
        menu1 -> 文件
        menu2 -> 帮助
        """
        self.begin_menu: Menu = Menu(self)
        self.config(menu = self.begin_menu)
        self.menu0 ,self.menu1 ,self.menu2 = Menu(self.begin_menu) ,Menu(self.begin_menu ,fg='#F307FF') ,Menu(self.begin_menu ,fg="#F307FF")
        self.menu3: Menu = Menu(self.menu2)
        
        #self.menu0.add_command(label="运行项" ,command=self.screen_run)
        self.menu1.add_command(label="新建项目" ,command=self.NewFile)
        self.menu1.add_command(label="打开项目" ,command=self.OpenFile)
        self.menu1.add_command(label="新建文件" ,command=self.AskSaveAsFileName)
        self.menu1.add_command(label="打开文件" ,command=self.AskOpenFileName)
        self.menu1.add_command(label="打开Gal" ,command=lambda : system(r"start {}".format(filedialog.askopenfilename())))
        self.menu1.add_command(label="测试Gal" ,command=self.__Screen_Run)
        self.menu1.add_command(label="关闭系统" ,command=self.destroy)
        
        self.menu2.add_command(label="关键字" ,command=lambda : TopRoot().text(TkMeta.Hint))
        self.menu2.add_command(label="关于" ,command=lambda : TopRoot().text(TkMeta.About))
        self.menu2.add_command(label="设置" ,command=test)
        self.menu2.add_command(label="隐藏" ,command=self.withdraw) #需改进
        self.menu2.add_command(label="转换" ,command=self.__ConvertMode) #未测试
        self.menu2.add_command(label="颜色" ,command=test)
        self.menu2.add_command(label="替换" ,command=self.__Replace)

        self.menu3.add_command(label="主循环" ,command=lambda : self.__Template(1))
        self.menu3.add_command(label="导入" ,command=lambda : self.__Template(2))
        self.menu3.add_command(label="*" ,command=lambda : test) #未实装
        
        self.bind("<Control-n>" ,lambda event : self.NewFile())
        self.bind("<Control-o>" ,lambda event : self.OpenFile())
        
        self.begin_menu.add_cascade(label="文件" ,menu=self.menu1)
        #self.begin_menu.add_cascade(label="运行" ,menu=self.menu0)
        self.begin_menu.add_cascade(label="帮助" ,menu=self.menu2)
        self.menu2.add_cascade(label="模板" ,menu=self.menu3)

        self.mainloop()
        

    def NewFile(self) -> NoReturn:
        self.__InitTempList()

        self.GetNameTxt: Label = Label(self ,text="请给项目起个名：")
        self.GetNameBar: Entry = ttk.Entry(self ,textvariable=self.NameVar)
        self.GetNameBtn: Button = ttk.Button(self ,text="OK" ,command=self.NewFileRun)

        Var: BooleanVar = BooleanVar()
        GetConfigTxt: Label = Label(self ,text="个性化选项:")
        GetConfigBar: ttk.Radiobutton = ttk.Radiobutton(self ,text="1-分辨率自适应" ,value=True ,variable=Var)
        GetConfigBar2: ttk.Radiobutton = ttk.Radiobutton(self ,text="2-高级创作模式")
        GetConfigBar3: ttk.Radiobutton = ttk.Radiobutton(self ,text="3-无报错模式")

        self.TempList: list = [self.GetNameTxt ,self.GetNameBar ,self.GetNameBtn ,GetConfigTxt ,GetConfigBar ,GetConfigBar2 ,GetConfigBar3]
        
        for index ,each in enumerate(self.TempList ,start=0):
            each.place(x=self.width//2-100 ,y=10+30*index)
        else:
            self.TempList.append(Var)


    def NewFileRun(self) -> NoReturn:
        """
        self.name first show
        """
        self.AutoResolution: bool = self.TempList.pop().get()
        self.name: str = self.NameVar.get()
        if path.exists(save_path := ''.join([TkWindow.basepath ,self.savepath ,self.name])):
            showerror("错误" ,"项目已存在！")
            return
        
        for index ,item in enumerate(self.TempList):
            item.destroy()
        else:

            if vars(self).get("MenuName" ,False):
                delattr(self ,"MenuName")
                showerror("错误" ,"项目已打开！")
                return
            
            mkdir(r"{}".format(save_path))
            for i ,e in enumerate({"pic" ,"csv" ,"bgm"}):
                mkdir(r"{}/{}".format(save_path ,e))

            TkWindow.info["AutoResolution"]: bool = self.AutoResolution
            TkWindow.info["dir"] ,TkWindow.info["name"] = save_path+"//" ,self.name
            with open(save_path+"//info.json" ,'w' ,encoding='utf-8') as file:
                json_dump(TkWindow.info ,file)

            self.__StaticRepair(self.name)

        self.MenuName: Menu = Menu(self.begin_menu)
        self.MenuName.add_command(label="打开Gal" ,command=self.OpenCsv)
        self.MenuName.add_command(label="测试Gal" ,command=self.screen_run)
        self.MenuName.add_command(label="新加项" ,command=self.AddFile)
        self.begin_menu.add_cascade(label=self.name ,menu=self.MenuName)
        TkWindow.Menu.append(self.MenuName)


    def OpenCsv(self) -> NoReturn:
        """
        before AddFile
        """
        path: str = TkWindow.basepath+f"//data//{self.name}//{self.name}.csv"

        if not TkWindow.Memory.get(path ,False):
            self.path: str = path
            self.database.creater(self.path)
            TkWindow.Memory[path] = True

        path: str = path if not self.__dict__.get("path" ,False) else self.path
        
        system(r"start {}".format(path))
        

    def AddFile(self) -> NoReturn:
        self.__InitTempList()
        
        NameVar: StringVar = StringVar()
        GetNameTxt: Label = Label(self ,text="请给文件起个名：")
        GetNameBar: Entry = ttk.Entry(self ,textvariable=self.FileVar) #FileVar
        GetNameBtn: Button = ttk.Button(self ,text="OK" ,command=self.SaveFile)
        GetNameTxt.place(x=self.width//2-100 ,y=10)
        GetNameBar.place(x=self.width//2-100 ,y=40)
        GetNameBtn.place(x=self.width//2-100 ,y=70)

        self.TempList: list[Menu ,Ellipsis] = [GetNameTxt ,GetNameBtn ,GetNameBar]


    def SaveFile(self) -> NoReturn:

        if not len(file_name := self.FileVar.get()): #updated!#
            showerror("错误" ,"文件名不可为空！")
            return

        gal_py: str = ''.join([TkWindow.basepath ,self.savepath ,self.name ,"//" ,file_name ,self.__suffix])

        if path.exists(target_file := ''.join([TkWindow.basepath ,self.savepath ,self.name ,"//" ,file_name ,".py"])):
            showerror("错误！" ,"文件已存在！")
            return

        header: str = GalPy.encode(f"# -*- coding: utf-8 -*-\n# -*- file: {file_name}.Gal♥Py -*-")
        
        with open(gal_py ,'w' ,encoding='utf-8' ,newline='') as file:
            file.write(header)
        
        def OpenFile() -> NoReturn:
            self.Text.delete('1.0' ,END)
            with open(gal_py ,'r' ,encoding='utf-8' ,newline='') as file:
                self.Text.insert('1.0' ,GalPy.decode(file.read()))
                
            self.target_file: str = file_name
            #self.target_file_label: Label = ttk.Label(self ,text=self.target_file)
            #self.target_file_label.place(x=self.width//2-10 ,y=3)
            self.Text.place(x=0 ,y=28)
            #self.x_bar.place(x=0 ,y=0)
            #self.y_bar.place(x=self.width-100 ,y=0)
            self.y_bar.pack(side=RIGHT ,fill=Y)
            if not self.AutoTagAddBtn:
                self.AutoTagAdd.start()
                self.AutoTagAddBtn: bool = True

        def SaveFile() -> NoReturn:
            text: str = self.Text.get('1.0' ,END)
            with open(gal_py ,'w' ,encoding='utf-8' ,newline='') as file:
                file.write(GalPy.encode(text))
            self.parser.get(text) << gal_py
            

        def RunFile() -> NoReturn:
            if not path.exists(gal_py):
                showerror("警告！" ,".Gal♥Py文件丢失！")
                          
            if not path.exists(target_file):
                showerror("致命性错误" ,".py文件丢失！\n请反译.Gal♥Py！")
                return

            screen: PyScreen = self.screen
            window: Self = self
            
            with open(target_file ,'r' ,encoding='utf-8' ,newline='') as file:
                # Run Module #
                TEXT: str = file.read()
                #self.withdraw()
                print(f"\n -*- {truename}"+self.__suffix+" -*-\n" ,strftime("-*- 运行开始: %H:%M:%S -*-") ,end="\n")
                
                if self.parser.RunScreenModule(TEXT):
                    RETURN: str = getcwd()
                    chdir(path.dirname(target_file))
                    system("{}".format(path.basename(target_file)))
                    chdir(RETURN)
                
                else:
                    exec(TEXT)

        for index ,each in enumerate(self.TempList):
            each.destroy()
            
        self.NextMenu()
        menu: Menu = Menu(self.begin_menu)
        menu.add_command(label="打开" ,command=OpenFile)
        menu.add_command(label="保存" ,command=SaveFile)
        menu.add_command(label="测试" ,command=RunFile)
        self.begin_menu.add_cascade(label=file_name ,menu=menu)
        TkWindow.File[file_name]: dict[str : Menu] = menu


    def OpenFile(self) -> NoReturn:
        self.__InitTempList()
        
        textvariable: StringVar = StringVar()
        values: dict[str:str] = {f"{index}.{path.basename(each)}":each for index ,each in enumerate(iglob(TkWindow.basepath+"//data//*") ,start=1)}
        combo: ttk.Combobox = ttk.Combobox(self ,values=list(values) ,textvariable=textvariable ,width=40)
        label: Label = ttk.Label(self ,text="请选择项目：")
        button: Button = ttk.Button(self ,text="OK" ,command=self.LoadFile)
        
        self.TempList.extend([label ,combo ,button])
        
        for index ,each in enumerate(self.TempList):
            each.place(x=self.width//2-100 ,y=10+30*index)
        else:
            self.TempList.append(textvariable)
            self.TempList.append(values)
        

    def LoadFile(self) -> NoReturn:
        values: dict[str:str] = self.TempList.pop()
        file_name: str = self.TempList.pop().get()
        self.name: str = file_name[file_name.index('.')+1:] # 1. 2.
        target_file: str = ''.join([TkWindow.basepath ,self.savepath ,self.name ,"//{}.py".format(self.name)])
        self.path: str = TkWindow.basepath+f"//data//{self.name}//{self.name}.csv"
        TkWindow.Memory[target_file[:-2]+"csv"]: dict = True

        if not len(self.name):
            showerror("致命性错误" ,"文件名不应为空！")
            return

            if len(TkWindow.File) or len(TkWindow.Menu):
                
                for index ,(key ,item) in enumerate(TkWindow.File.items() ,start=0):
                    item.destroy()
                    TkWindow.Menu.destroy()
                else:
                    TkWindow.File.clear()
                    TkWindow.Menu.clear()

        if not len(save_path := glob(''.join([TkWindow.basepath ,self.savepath ,self.name ,"//*.json"]))):
            showerror("错误" ,"唯一指定json丢失或重复！")
            return
        
        with open(save_path[0] ,'r' ,encoding='utf-8') as file:
            TkWindow.info: dict = json_load(file)

        if TkWindow.info["Version"] != __VERSION__:
            showerror("版本错误" ,"暂不版本兼容！")
            return

        self.MenuName: Menu = Menu(self.begin_menu)
        self.MenuName.add_command(label="打开" ,command=self.OpenCsv)
        self.MenuName.add_command(label="测试" ,command=self.screen_run)
        self.MenuName.add_command(label="新加项" ,command=self.AddFile)
        self.begin_menu.add_cascade(label=self.name ,menu=self.MenuName)
        TkWindow.Menu.append(self.MenuName)

        for i ,e in enumerate(self.TempList):
            e.destroy()

        if not len(glob(TkWindow.basepath + self.savepath + self.name + r"//*"+self.__suffix)):
            return
        
        menu_: Menu = Menu(self.begin_menu)
        self.begin_menu.add_cascade(label="→" ,menu=menu_)

        fromlist: list = glob(values[f"{file_name}"]+r"//*"+self.__suffix)
        
        for index ,each in enumerate(fromlist ,start = 1):

            name: str = path.basename(each)
            truename: str = name[:name.index('.')]

            def OpenFile() -> NoReturn:
                print(f"{name=}")
                print(f"{truename=}")
                print(f"{each=}")

                
                self.Text.delete('1.0' ,END)

                target_file: str = each
            
                with open(target_file ,'r' ,encoding='utf-8' ,newline='') as file:
                    self.Text.insert('1.0' ,GalPy.decode(file.read()))
                    
                self.target_file: str = truename
                #self.target_file_label: Label = ttk.Label(self ,text=self.target_file)
                #self.target_file_label.place(x=self.width//2-10 ,y=3)
                self.Text.place(x=0 ,y=28)
                self.y_bar.pack(side=RIGHT ,fill=Y)
                if not self.AutoTagAddBtn:
                    self.AutoTagAdd.start()
                    self.AutoTagAddBtn: bool = True

            def SaveFile() -> NoReturn:
                target_file: str = each
                text: str = self.Text.get('1.0' ,END)
                with open(target_file ,'w' ,encoding='utf-8' ,newline='') as file:
                    file.write(GalPy.encode(text))
                self.parser.get(text) << each

            def RunFile() -> NoReturn:
                if not path.exists(each):
                    showerror("警告！" ,".Gal♥Py文件丢失！")

                target_file: str = each[:each.index('.')]+".py"
                if not path.exists(target_file):
                    showerror("致命性错误" ,".py文件丢失！\n请将.Gal♥Py反编译！")
                    return

                screen: PyScreen = self.screen
                window: Self = self
                
                with open(target_file ,'r' ,encoding='utf-8' ,newline='') as file:
                    # Run Module #
                    TEXT: str = file.read()
                    #self.withdraw()
                    print(f"\n -*- {truename}"+self.__suffix+" -*-\n" ,strftime("-*- 运行开始: %H:%M:%S -*-") ,end="\n")
                    
                    if self.parser.RunScreenModule(TEXT):
                        RETURN: str = getcwd()
                        chdir(path.dirname(target_file))
                        system("{}".format(path.basename(target_file)))
                        chdir(RETURN)
                    
                    else:
                        exec(TEXT)
                    
                print(strftime(" -*- 运行结束: %H:%M:%S -*-") ,end="\n\n")
            
            menu ,menu_ = Menu(self.begin_menu) ,Menu(self.begin_menu)
            menu.add_command(label="打开" ,command=OpenFile)
            menu.add_command(label="保存" ,command=SaveFile)
            menu.add_command(label="测试" ,command=RunFile)
            self.begin_menu.add_cascade(label=truename ,menu=menu)
            TkWindow.File[truename]: dict[str : Menu] = menu

            if index.__ne__(len(fromlist)):
                self.begin_menu.add_cascade(label="→" ,menu=menu_)
                TkWindow.Menu.append(menu_)
            
        #TkWindow.Menu.pop().destroy()


    def TagAdd(self) -> NoReturn:

        #_Memory: dict[str : list[str]] = dict(zip(self.KeyWords ,[]))
        Memory: set = set()
        _Memory: set = set()
        start: str = '1.0'
        target: set = Memory
        begin: str = ''
        
        while True:

            try:
            
                for index ,(each ,color) in enumerate(self.KeyWords.items() ,start=0):

                    Begins: list = re_findall(r"({})".format(each) ,self.Text.get('1.0' ,END))

                    #if not (listlen := len(Begins)):
                    #    break

                    for _ in range(len(Begins)):
                        if begin := self.Text.search(each ,start):
                            #name: str = str(index)
                            end: str = str(eval(begin)+len(each)*0.1)
                            self.Text.tag_add(str(index) ,begin ,end)
                            self.Text.tag_config(str(index) ,foreground=color)
                            target.add(str(index))
                            start: str = end

                    if not begin:
                        if Memory and _Memory:
                            d1 ,d2 = Memory.difference(_Memory) ,_Memory.difference(Memory)
                            for index ,each in enumerate({*d1 ,*d2}):
                                self.Text.tag_delete(each)
                        if Memory.__len__().__gt__(100) or _Memory.__len__().__gt__(100):
                            Memory.clear()
                            _Memory.clear()

                sleep(0.7)
                target: set = Memory if target != Memory else _Memory

            except Exception as ERROR:
                #print(ERROR)
                return
        

    def _Open(self) -> NoReturn:
        pass
    

    def _Init(self) -> NoReturn:
        pass


    def NextMenu(self) -> NoReturn:
        menu: Menu = Menu(self.begin_menu)
        self.begin_menu.add_cascade(label="→" ,menu=menu)
        TkWindow.Menu.append(menu)


    def ReturnMenu(self) -> NoReturn:
        TkWindow.Menu.pop()


    def AutoSpace(self) -> NoReturn:
        self.Text.insert(self.Text.index(INSERT) ,"    ")


    def AskOpenFileName(self) -> NoReturn:

        if (filename := filedialog.askopenfilename()) is None:
            showerror("错误" ,"打开文件失败！")
            return

        basename: str = path.basename(filename)
        truename: str = basename[:basename.index('.')]

        self.__InitTempList()
        
        if basename[basename.index('.'):] != self.__suffix:
            showerror("错误" ,f"不是{self.__suffix}文件！")
            return
        
        def OpenFile() -> NoReturn:
            
            self.Text.delete('1.0' ,END)
        
            with open(filename ,'r' ,encoding='utf-8' ,newline='') as file:
                self.Text.insert('1.0' ,GalPy.decode(file.read()))
                
            #self.target_file: str = truename
            #self.target_file_label: Label = ttk.Label(self ,text=self.target_file)
            #self.target_file_label.place(x=self.width//2-10 ,y=3)
            self.Text.place(x=0 ,y=28)
            self.y_bar.pack(side=RIGHT ,fill=Y)
            if not self.AutoTagAddBtn:
                self.AutoTagAdd.start()
                self.AutoTagAddBtn: bool = True

        def SaveFile() -> NoReturn:
            text: str = self.Text.get('1.0' ,END)
            with open(filename ,'w' ,encoding='utf-8' ,newline='') as file:
                file.write(GalPy.encode(text))
            self.parser.get(text) << filename

        def _RunFile() -> NoReturn:
            if not path.exists(filename):
                showerror("警告！" ,".Gal♥Py文件丢失！")

            target_file: str = filename[:filename.index('.')]+".py"
            if not path.exists(target_file):
                showerror("致命性错误" ,".py文件丢失！\n请将.Gal♥Py反编译！")
                return

            screen: PyScreen = self.screen
            window: Self = self
         
            with open(target_file ,'r' ,encoding='utf-8' ,newline='') as file:
                # Run Module #
                TEXT: str = file.read()
                #self.withdraw()
                print(f"\n -*- {truename}"+self.__suffix+" -*-\n" ,strftime("-*- 运行开始: %H:%M:%S -*-") ,end="\n")

                #print(f"{self.parser.RunScreenModule(TEXT)=}")
                
                if self.parser.RunScreenModule(TEXT):
                    RETURN: str = getcwd()
                    chdir(path.dirname(filename))
                    system("{}".format(path.basename(target_file)))
                    chdir(RETURN)
                
                else:
                    exec(TEXT)
                    
                print(strftime(" -*- 运行结束: %H:%M:%S -*-") ,end="\n\n")
                #self.deiconify()

        def RunFile() -> NoReturn:
            run_file: Any = Thread(target=_RunFile ,name="RunFile")
            run_file.start()
            #run_file.join()

        self.NextMenu()
        menu: Menu = Menu(self.begin_menu)
        menu.add_command(label="打开" ,command=OpenFile)
        menu.add_command(label="保存" ,command=SaveFile)
        menu.add_command(label="测试" ,command=_RunFile)
        self.begin_menu.add_cascade(label=truename ,menu=menu)
        TkWindow.File[truename]: dict[str : Menu] = menu


    def AskSaveAsFileName(self) -> NoReturn:
        if (save_path := filedialog.asksaveasfilename()) is None:
            showerror("错误" ,"文件名字不应为空！")
            return

        self.__InitTempList()

        save_path: str = save_path[:save_path.index('.')] if '.' in save_path else save_path
        save_path += self.__suffix

        basename: str = path.basename(save_path)
        truename: str = basename[:basename.index('.')]

        with open(save_path ,'w' ,encoding='utf-8' ,newline='') as file:
            file.write(GalPy.encode(f"# -*- coding: utf-8 -*-\n# -*- file: {truename}.Gal♥Py -*-"))

        def OpenFile() -> NoReturn:
            
            self.Text.delete('1.0' ,END)
        
            with open(save_path ,'r' ,encoding='utf-8' ,newline='') as file:
                self.Text.insert('1.0' ,GalPy.decode(file.read()))
                
            self.Text.place(x=0 ,y=28)
            self.y_bar.pack(side=RIGHT ,fill=Y)
            if not self.AutoTagAddBtn:
                self.AutoTagAdd.start()
                self.AutoTagAddBtn: bool = True

        def SaveFile() -> NoReturn:
            text: str = self.Text.get('1.0' ,END)
            with open(save_path ,'w' ,encoding='utf-8' ,newline='') as file:
                file.write(GalPy.encode(text))
            self.parser.get(text) << save_path

        def _RunFile() -> NoReturn:
            if not path.exists(save_path):
                showerror("警告！" ,".Gal♥Py文件丢失！")

            target_file: str = save_path[:save_path.index('.')]+".py"
            if not path.exists(target_file):
                showerror("致命性错误" ,".py文件丢失！\n请将.Gal♥Py反编译！")
                return

            screen: PyScreen = self.screen
            window: Self = self
          
            with open(target_file ,'r' ,encoding='utf-8' ,newline='') as file:
                # Run Module #
                TEXT: str = file.read()
                #self.withdraw()
                print(f"\n -*- {truename}"+self.__suffix+" -*-\n" ,strftime("-*- 运行开始: %H:%M:%S -*-") ,end="\n")
                
                if self.parser.RunScreenModule(TEXT):
                    RETURN: str = getcwd()
                    chdir(path.dirname(save_path))
                    system("{}".format(path.basename(target_file)))
                    chdir(RETURN)
                
                else:
                    exec(TEXT)
                    
                print(strftime(" -*- 运行结束: %H:%M:%S -*-") ,end="\n\n")
                

        self.NextMenu()
        menu: Menu = Menu(self.begin_menu)
        menu.add_command(label="打开" ,command=OpenFile)
        menu.add_command(label="保存" ,command=SaveFile)
        menu.add_command(label="测试" ,command=_RunFile)
        self.begin_menu.add_cascade(label=truename ,menu=menu)
        TkWindow.File[truename]: dict[str : Menu] = menu


    def __InitTempList(self) -> NoReturn:
        if self.TempList:
            for index ,each in enumerate(self.TempList):
                try:
                    each.destroy()
                except Exception as ERROR:
                    #print(ERROR)
                    pass
            self.TempList.clear()


    def __StaticRepair(self ,name: str) -> NoReturn:
        if not path.exists(dirpath := mainpath+datapath+f"{name}//GalPy"):
            mkdir(dirpath)
            if not glob(dirpath+"//*.py").__len__():
                for index ,each in enumerate(iglob(r"GalPy//*.py") ,start=1):
                    basename: str = path.basename(each)
                    name: str = basename[:basename.index('.')]
                    with open(each ,"r" ,encoding="utf-8") as reader ,open(dirpath+f"//{name}.py" ,"w" ,encoding='utf-8') as writer:
                        writer.write(reader.read())


    def __Template(self ,option: int) -> NoReturn:
        with open(self.Template[option] ,"r" ,encoding="utf-8") as file:
            self.Text.insert(END ,"\n"+file.read())


    @property
    def __isTemplateExists(self) -> bool:
        return all([path.exists(each) for index ,(key ,each) in enumerate(self.Template.items() ,start=0)])


    def __ConvertMode(self) -> NoReturn:
        if not path.exists(filename := filedialog.askopenfilename()):
            showerror("错误" ,"请选择正确的路径！")
            return

        file: str = path.basename(filename)
        suffix: str = file[file.index('.')-1:]

        self.__Convert(filename = filename ,mode = suffix)


    def __Convert(self ,* ,filename: str ,mode: str) -> NoReturn:
        mode: str = ".py" if (convert := mode.__eq__(self.__suffix)) else self.__suffix

        with open(filename[:filename.index('.')]+mode ,"w" ,encoding="utf-8") as ee ,open(filename ,"r" ,encoding="utf-8") as er:
            ee.write(GalPy.decode(er.read()) if convert else GalPy.encode(er.read()))

        showinfo("通知" ,"转换成功！")


    def __AskColor(self) -> NoReturn:
        pass


    def __Screen_Run(self) -> NoReturn:
        if not self.__dict__.get("screen" ,False):
            delattr(self ,"screen")
            showerror("错误" ,"屏幕尚未初始化！")
            return

        if not (_path := filedialog.askopenfilename()) or _path[_path.index('.'):].__ne__(".csv"):
            showerror("错误" ,"打开文件的格式错误！")
            return

        self.database.fmt_path: str = _path
        path_: str = '//'.join(_path.split('/')[:-1])+"\\"

        #print(f"__Screen_Run：{_path=}\n{path_}")

        (self.screen << self.database.reader(_path ,path_=path_)).action()

        self.screen.reinit()


    def __Replace(self) -> NoReturn:
        ReplacedText: str = self.Text.get("1.0" ,END).replace(input("请输入被替换的内容：") ,input("请输入替换的内容："))
        self.Text.delete("1.0" ,END)
        self.Text.insert("1.0" ,ReplacedText)
    

async def MAIN(*args: tuple[Any] ,**kwargs: dict[Any]) -> Any:
    window: TkWindow = TkWindow()
    screen: PyScreen = PyScreen("This Is Test!" ,(100 ,100))
    window << screen
    window.start()


def main(*args: tuple[Any] ,**kwargs: dict[Any]) -> NoReturn:
    asyncio.run(MAIN(*args ,**kwargs))


if __name__ == "__main__":
    main()
    #print('\\'.join(r"C:\Users\sfuch\Desktop\Gal♥Py\data\TEST\TEST.csv".split('\\')[:-1]) + "\\")




