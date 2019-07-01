#-*-coding:utf-8 -*-
info={'name':'zyl','age':24,'high':175}
while True:
    print('='*60)
    print("===名片管理系统===")
    print("1.修改 2.删除 3.查询 4.增加 5.退出")
    C=input("请选择:")
    if C=="1":
        res = input("请输入需要修改的关键词:")
        if res=="name":
            info['name']=input('请输入相关的内容:')
            print(info)
        elif res=="age":
            info['age']=input('请输入相关的内容:')
            print(info)
        elif res=="high":
            info['high']=input('请输入相关的内容:')
            print(info)
    if C=='2':
        res1=input("请输入需要删除的关键词:")
        print(info.pop(res1))
        print(info)
    if C=='3':
        res2=input("请输入需要查询的关键词:")
        print(info.get(res2))
    if C=='4':
        res3=input("请输入需要增加的关键词:")
        v1=input("请输入关键词内容:")
        print(info.update({}.fromkeys((res3,),v1)))
        print(info)
    if C=='5':
        print("退出本次操作")
        exit()