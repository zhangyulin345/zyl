#-*- coding:UTF-8 -*-
l1=[]
while True:
    print('*'*60)
    print('==============欢迎进入名片管理系统==============')
    print('1.查看名片')
    print('2.添加名片')
    print('3.修改名片')
    print('4.删除名片')
    print('5.退出系统')
    choose=input('请选择:')
    if choose=='1':
        i=0
        while  i<len(l1):
            print('%s-->姓名: %s|年龄: %s|身高: %s' %(i,l1[i]['name'],l1[i]['age'],l1[i]['high']))
            i+=1
        else:
            print('空')
    elif choose=='2':
        name=input('name:').strip()
        age=input('age:').strip()
        high=input('high:').strip()
        info={'name':name,
             'age':age,
             'high':high}
        l1.append(info)
        print('添加成功')
    elif choose=='3':
        revise=input('请输入需要修改的名片:')
        name1=input('name:').strip()
        age1=input('age:').strip()
        high1=input('high:').strip()
        if name1:
            l1[int(revise)]['name']=name1
        if age1:
            l1[int(revise)]['age']=age1
        if high:
            l1[int(revise)]['high']=high1
        print('名片修改成功')
    elif choose=='4':
        revise2=input('请输入要删除的名片:')
        l1.remove(l1[int(revise2)])
        print("删除成功")
    elif choose=='5':
        print("退出系统")
        break
    else:
        print("输入错误，请重新输入")