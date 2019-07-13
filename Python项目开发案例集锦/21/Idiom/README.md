### 项目介绍
小程序因其“用完即走”的特性备用用户欢迎，其中各种答题类的小程序因具备一定的趣味性而异常火爆，下面，我们就模拟猜成语小程序，开发一款寓教于乐的“看图猜成语小程序”。
闲言少叙，上图看效果。



![登录页.png | center | 265x475](https://cdn.nlark.com/yuque/0/2018/png/130433/1544135816482-b492dd51-0de2-4ab1-9104-9622d13e7334.png "")



![首页.png | center | 263x470](https://cdn.nlark.com/yuque/0/2018/png/130433/1544136006720-97563ed3-ee18-4b56-bceb-fe30c769cfba.png "")



![答题页.png | center | 259x456](https://cdn.nlark.com/yuque/0/2018/png/130433/1544136034498-b2f5f86f-33a0-4cb9-a823-2ef2d8eff09f.png "")



![通关页.png | center | 258x449](https://cdn.nlark.com/yuque/0/2018/png/130433/1544136051491-9c393935-beb6-494c-9893-38a9213e779a.png "")



![分享页.png | center | 259x451](https://cdn.nlark.com/yuque/0/2018/png/130433/1544136065403-f30d9f02-895c-4ec7-b052-ad9e3184ae97.png "")



![排行榜页.png | center | 251x433](https://cdn.nlark.com/yuque/0/2018/png/130433/1544136072075-b52e9801-191c-4b32-956d-b6573a3e0965.png "")




### 基本技能要求：
* flask 基础知识
* 小程序基础知识

### 开发及运行环境：
* 虚拟环境：virtualenv。
* 数据库：PyMySQL驱动+ MySQL。
* 开发工具：微信开发者工具+PyCharm / Sublime Text 3。
* PythonWeb 框架：Flask。
* 接口调试工具：Postman。

### 数据库设计：
本项目采用MySQL数据库，数据库名称为idiom。在小程序中涉及用户信息和题目信息，所以在idom数据库下包含2张数据表，数据表名称及作用如下：
* user表：存储用户信息，包括用户昵称、头像和排名等。
* exam表：存储题目信息，包括图片、答案和备选项等。

### 使用说明
1. 使用pip安装virtualenv，命令如下：
```
pip install virtualenv
```
2. 在“flask/”目录下，创建venv 虚拟环境，命令如下：
```
virtualenv  venv
```
3. 启动虚拟环境，
windows下命令如下：
```
venv\scripts\activate
```
mac下命令如下：
```
source venv\bin\activate
```
4. 安装依赖，命令如下：
```
pip install -r requirements.txt
```
5. 创建数据库，命名为idom
6. 使用数据迁移命令
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
7. 创建完数据表后，将“flask\idiom.sql”文件导入到数据库
8. 启动python,运行如下命令：
```
python manage.py runserver
```
9. 开启小程序调试工具，新建项目，项目目录是“idiom/weapp-idiom”。

