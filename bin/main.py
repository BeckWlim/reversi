background_image_filename = 'image/background.jpg'
mouse_image_filename = 'image/blackChess.png'
#指定图像文件名称

import pygame
# 导入pygame库
from pygame.locals import *
# 导入一些常用的函数和常量
from sys import exit
# 向sys模块借一个exit函数用来退出程序\
from module.window import MainWindow

mainWindow = MainWindow()
mainWindow.render()




