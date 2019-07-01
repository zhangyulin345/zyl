#-*- coding:UTF-8 -*-
import random
lost=0
win=0
ping=0
while True:
    print('=' * 60)
    print('****************欢迎来猜拳*****************')
    print('赢:%s     平:%s        输:%s'%(win,ping,lost))
    print('1.石头  2.剪刀   3.布  4.退出')
    rebot=random.choice(['石头','剪刀','布'])
    h=input("请出")
    if (h=='1' and rebot=='剪刀') or (h=='2' and rebot=='布') or (h=='3' and rebot=='石头'):
        win+=1
        print("YOUR ARE WINER")
    elif (h=='1' and rebot=='石头') or (h=='2' and rebot=='剪刀') or (h=='3' and rebot=='布'):
        ping+=1
        print("YOUR ARE PINGER")
    elif (h=='1' and rebot=='布') or (h=='2' and rebot=='石头') or (h=='3' and rebot=='剪刀'):
        lost+=1
        print("YOUR ARE LOSTER")
    elif h=='4':
        print("退出")
        break
    else:
        print("输入有误")