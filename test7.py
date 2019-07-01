#-*- coding=UTF-8 -*-
print("-----欢迎登录-----:")
info={'zyl':'zyl123',
     'wn':'wn134',
      'zmx':'zmx123'}
count=0
print('1、登录 2、注册')
while True:
    choose=input('请选择登录or注册:')
    if choose=='1':
        user=input('用户名:')
        with open(r'/home/zyl/a.txt','r',encoding='utf-8') as f:
            data=f.read()
            if user in data:
                print('滚蛋吧')
                break
        pwd=input('密码:')
        if info[user]==pwd:
            print('登录成功')
        else:
            count+=1
            print('密码错误')
            if count==3:
                with open(r'/home/zyl/a.txt','w',encoding='utf-8') as f:
                    f.write(user)
                    print('你的账号被封了')
                    break
    if choose=='2':
        user1=input("请输入用户名:")
        psw1=input("请输入密码:")
        info.setdefault(user1,psw1)
        print(info)
        break
