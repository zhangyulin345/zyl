# -*- coding: utf-8 -*-
import os
import sys
import time

# 导入Pygame
try:
    import pygame
except ModuleNotFoundError:
    print('正在安装pygame，请稍等...')
    os.system('pip install pygame') # 安装pygame模块
import tools # 导入tools模块

# 检测Python版本号
__MAJOR, __MINOR, __MICRO = sys.version_info[0], sys.version_info[1], sys.version_info[2]
if __MAJOR < 3:
    print('Python版本号过低，当前版本为 %d.%d.%d， 请重装Python解释器' % (__MAJOR, __MINOR, __MICRO))
    time.sleep(2)
    exit()

if __name__ == '__main__':
    # 创建Paint类的对象
    paint = tools.Paint()
    try:
        paint.run()  # 启动主窗口
    except Exception as e:
        print(e)