$include *
$define NAME 
$define WIDTH
$define HEIGHT

from * import *

screen: PyScreen = PyScreen(NAME ,(0 ,0))
screen.width: int = WIDTH
screen.height: int = HEIGHT

#screen.init()
