# -*- coding: utf-8 -*-

import pygame
from random import shuffle ,choice
from re import findall
from pygame.locals import *
from typing import Any ,NewType ,NoReturn ,Callable
from functools import partial
from time import sleep
from collections import deque
from glob import glob
from tkinter.messagebox import showerror
from os import path

function: Callable = partial
PAUSE: Callable = sleep
TIME: Callable = pygame.time.Clock

EVENTS: Any = pygame.event.get
KEYS: Any = pygame.key.get_pressed
ALLOW: Any = pygame.event.set_allowed

KEY: dict = dict(zip([chr(key).upper() for key in range(97 ,123)] ,[key for key in range(97 ,123)]))

class PyScreen(object):
    """
    shot  ->  back  ->  main  ->  text
    song ,animation

    self.say  ->  self.TEXT : Callable
    self.pic  ->  self.BACK : Callable
    self.pic  ->  self.MAIN : Callable

    self.shot : dict
    self.back : str  ->  ["back"] -> str
    self.main : str  ->  ["main"] -> list *
    self.text : str  ->  ["text"] -> str
    self.play : str  ->  ["play"] -> str
    """

    Defaults: dict = {
                "AutoResolution" : False
            }

    def add_experimental_option(self ,option: str ,default: Any) -> bool:
        if not option in list(PyScreen.Defaults):
            showerror("错误" ,"没有此选项!")
            return

    def reinit(self) -> NoReturn:
        self.pointer: int = 0b0
        self.run: bool = True
        

    def __init__(self ,name:str ,w_h:tuple|list ,* ,path: str = '') -> NoReturn:
        #self.AllPic = glob(r"data/pic/*")
        self.pointer ,self.run = 0 ,True
        #self.rebind() #%$%#
        self.name: str = name
        self.width_ ,self.height_ = w_h
        self.path: str = path
        self.database: Any = None
        self.basepath: str = '//'.join(__file__.split('\\')[:-2])
        self.width = self.height = ''
        self.play: Any = None
        self.font: str = "幼圆"
        self.TEXT: Callable = partial(self._say ,size=40 ,color=(255 ,255 ,0) ,auto=0)
        self.MAIN: Callable = partial(self.pic ,pixel=True ,resize=False ,colorkey=False)# ,animation=False)
        self.BACK: Callable = partial(self._pic)
        self.CHAR: Callable = self.BACK


    def set(self ,name: str ,value: Any) -> NoReturn:
        setattr(self ,name ,value)


    def start(self ,name: str) -> NoReturn:
        """
        refer to self ,not use in arche-program!
        """
        #path_: str = ''.join([self.basepath ,"//data//" ,name ,'\\'])
        #name: str = ''.join([self.basepath ,"//data//" ,f"{name}//{name}.csv"])
        pass
        


    def __lshift__(self ,data: list[dict[Any]]) -> NoReturn:
        self.data: list = data
        self.rebind()
        pygame.init()
        self.width ,self.height = self.getPicSize(self.back) # using AllPic
        self.init()
        return self
        

    def init(self ,width: int = None ,height: int = None):
        pygame.init()
        if not self.__dict__.get("width" ,False):
            w ,h = width ,height
            delattr(self ,"width")
        else:
            w ,h = self.width ,self.height
            
        self.screen = pygame.display.set_mode((w ,h) ,vsync=True)
        pygame.display.set_caption(self.name)
        

    @staticmethod
    def flash():
        pygame.display.flip()
        

    def show_all_path(self ,data:str ,mode:str="pic") -> str:
        All = self.AllPic if mode == "pic" else MyMixer.AllBgm
        for index ,each in enumerate(All):
            if len(findall(data ,each)) != 0:
                return self.path + data + each[each.index('.'):]
        return -1
    

    def rebind(self):
        self.shot = self.data[self.pointer]
        self.back = self.shot["back"]          # back name
        self.main = self.shot["main"].split()  # char name
        self.text = self.shot["text"]           # just text
        self.play = self.shot["play"]           # just play_name
        #self.code = self.shot["code"]           # just function

        print(f"self.shot:{self.shot}")
        print(f"self.back_:{self.back} ,type:{type(self.back)}")
        print(f"self.main:{self.main}")
        #print(f"self.song_:{self.song_}")
        print(f"self.text:{self.text}\n")

        """
        if self.song != str(self.shot["song"]) and str(self.shot["song"]) not in ['' ,'#']: #   !   #
            self.song = str(self.shot["song"])          # song name
            print(f"self.song:{self.song}\nsong type:{type(self.song)}")
            self.mixer << self.song
            self.mixer >> 0
        else:
            pass
        """

        #self.back = self.show_all_path(self.back_)                      # all path back
        #self.main = [self.show_all_path(each) for each in self.main_]   # all path main

        print(f"back:{self.back}\nmain:{self.main}")
        

    def pic_info(self ,add ,**pic:dict) -> tuple:  # @set pic info@ #
        init = pygame.image.load(add).convert_alpha() if pic["pixel"] else pygame.image.load(add).convert()
        new = pygame.transform.rotozoom(init ,pic["angle"] ,pic["ratio"]) if pic["resize"] else init
        new.set_colorkey(pic["color"]) if pic["colorkey"] else None
        return (new ,new.get_width() ,new.get_height())
    

    def simple_pic(self ,new:str ,width:int ,height:int ,auto:bool=False): # @pic photo@ #
        if self.num_pic == 1:
            w ,h = (self.width-width)//2 ,self.height-height
        else:
            w ,h = self.num_pic_x ,self.height-height
        self.screen.blit(new ,(w ,h))
        if auto: PyScreen.flash()

        
    def _simple_pic(self ,
                   address:str ,
                   x:int ,
                   y:int ,
                   * ,
                   alpha:int = 255 ,
                   ratio:float = 1.0
                   ) -> NoReturn:
        picture = pygame.image.load(address).convert_alpha()
        photo = pygame.transform.rotozoom(picture ,0 ,ratio)
        photo.set_alpha(alpha)
        self.screen.blit(photo ,(x ,y))


    def dye(self ,**dye_info) -> NoReturn:
        try:
            color:tuple = dye_info["color"]
        except KeyError as KE:
            pass
        else:
            self.screen.fill(color)


    def fill(self ,color: tuple) -> NoReturn:
        self.screen.fill(color)


    def pic(self ,add:str|list ,**pic:dict): # @main pic@ #
        addList = [add] if isinstance(add ,str) else add if isinstance(add ,list) else None
        if addList is None:
            raise AttributeError("pic_address should be list OR str!")
        self.num_pic = len(addList)
        xp = self.width // (self.num_pic+1)
        for index ,each in enumerate(addList ,start=1):
            self.num_pic_x = xp * index - 18 * (self.num_pic - index)
            self.simple_pic(*self.pic_info(each ,**pic))
            
        
    def _pic(self ,add:str ,x:int ,y:int): #animation pic -> comic
        picture = pygame.image.load(add)
        match self.play: 
            case "fadeout"|"fadein"|"fade":
                for index ,each in enumerate(range(0 ,200 ,5)):
                    picture.set_alpha(each)
                    self.screen.blit(picture ,(x ,y))
                    PyScreen.flash()
                else:
                    print(f"Pic Animation Show Done!\nAll Index is {index}")
            case _:
                self.screen.blit(picture ,(x ,y))
        

    def say(self ,
            text: str ,
            x: int ,
            y: int ,
            * ,
            size: int ,
            color: tuple ,
            auto: bool = False
            ) -> NoReturn:
        """
        if not self.__dict__.get("font" ,False):
            delattr(self ,"font")
            showerror("错误" ,"font属性未设置！")
            return
        """
        self.screen.blit(pygame.font.SysFont(self.font ,size).render(text ,True ,color) ,(x ,y))
        PyScreen.flash() if auto else None


    def _say(self ,
             text: str ,
             x: int ,
             y: int ,
             * ,
             size: int ,
             color: tuple ,
             auto: bool=False 
             ) -> NoReturn: #animation say -> said
        _x ,_y = x ,y
        for index ,char in enumerate(text):
            _x ,_y = (x ,_y+46) if _x >= self.width-x else (_x ,_y)
            self.say(char ,_x ,_y ,size=size ,color=color ,auto=auto)
            PyScreen.flash()
            _x += 33
            sleep(0.04)
        else:
            #print(f"Say Animation Show Done!")
            pass


    def simple_say(self ,
                   text: str ,
                   x: int ,
                   y: int ,
                   color: tuple = (255 ,255 ,255) ,
                   size: int = 28
                   ) -> NoReturn:

        self.say(text=text ,x=x ,y=y ,size=size ,color=color)


    def action(self) -> NoReturn:
        clock ,self.key = pygame.time.Clock() ,True
        self.TEXT = partial(self._say ,size=40 ,color=(255 ,255 ,0) ,auto=0)
        self.MAIN = partial(self.pic ,pixel=True ,resize=False ,colorkey=False)# ,animation=False)
        #self.BACK = partial(self.pic ,pixel=False ,resize=False ,colorkey=False)
        self.BACK = partial(self._pic)
    
        while self.run:

            clock.tick(30)
            pygame.event.set_allowed([MOUSEBUTTONDOWN ,KEYDOWN ,QUIT])
            
            if self.key:
                self.BACK(self.back ,0 ,0)
                self.MAIN(self.main)
                self.TEXT(self.text ,80 ,self.height-100)
                PyScreen.flash()
                self.key = False

            for event in pygame.event.get():
                match event.type:
                    case pygame.MOUSEBUTTONDOWN:
                        x ,y = event.pos
                        print(f"x:{x}\ny:{y}")
                        self.pointer += 1
                        self.key = True
                        try:
                            self.rebind()
                        except:
                            print("\nShow Well Done!")
                            self.run = not self.run
                            sleep(1)
                            pygame.quit()
                            break
                            
                    case pygame.QUIT:
                        self.run = not self.run
                        break #pass
                    case pygame.KEYDOWN:
                        KEYS = pygame.key.get_pressed()
                        pass
                    case _:
                        pass
            else: pass 
        else: pass
        

    def _getPicSize(self ,name:str) -> tuple:
        for each in self.AllPic:
            if name in each:
                pic_info = pygame.image.load(each)
                return (pic_info.get_width() ,pic_info.get_height())
        else:
            raise FileNotFoundError("Error!")

    def getPicSize(self ,name:str) -> tuple:
        pic_info = pygame.image.load(name)
        return (pic_info.get_width() ,pic_info.get_height())


    @staticmethod
    def quit() -> NoReturn:
        pygame.quit()

    def __del__(self) -> str:
        return "屏幕关闭中..."


class SimpleMixer(object):

    def __init__(self ,
                 fromlist:list[str] ,
                 * ,
                 vol:float=0.6
                 ) -> NoReturn:
        """
        function SimpleMixer.__init__
            first initialize mixer
        """
        super(SimpleMixer ,self).__init__()
        pygame.mixer.init()
        self.fromlist:list[str] = fromlist
        self.running:bool = True
        self.length:int = len(self.fromlist)
        self.pointer:int = randint(0 ,self.length-1)
        pygame.mixer.music.set_volume(vol)

    def air(self ,music:str) -> NoReturn:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(1)

    def run(self) -> NoReturn:
        while self.running:
            try:
                if not pygame.mixer.music.get_busy():
                    self.air(self.fromlist[self.pointer])
                    self.pointer:int = (self.pointer + 0b1) % self.length
                sleep(3.8)
            except:
                return


class SimpleEffect(object):

    def __init__(self ,
                 fromlist:str ,
                 * ,
                 init:bool=False
                 ) -> NoReturn:
        """
        function SimpleEffect.__init__
            init in SimpleMixer
        """
        self.dict: dict = {}
        if init:
            pygame.mixer.init()
        for index ,each in enumerate(iglob(fromlist+"//*")):
            basename: str = path.basename(each)
            truename: str = basename[:basename.index('.')]
            self.dict[truename]: dict[str:str] = each


    def effect(self ,
               act:str ,
               * ,
               vol:int = 1.2
               ) -> NoReturn:

        effect = pygame.mixer.Sound(self.dict[act])
        effect.set_volume(vol)
        effect.play()


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





