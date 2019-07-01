#-*- coding:UTF-8 -*-
import threading
from time import ctime,sleep
def music(func):
    for i in range(2):
        print("I was listening to %s. %s" %(func,ctime()))
        sleep(1)
def move(func):
