from window import Ui_MainWindow  # 导入主窗体ui类
# 导入PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys  # 导入系统模块
import time, datetime  # 导入时间模块
from chart import PlotCanvas    # 导入自定义画图类
from query_request import *     # 导入自定义网络查询模块


# 显示消息提示框，参数title为提示框标题文字，message为提示信息
def messageDialog(title, message):
    msg_box = QMessageBox(QMessageBox.Warning, title, message)
    msg_box.exec_()

# 出窗体初始化类
class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)   # 默认显示车票查询
        self.model = QStandardItemModel();  # 创建存储数据的模式
        # 根据空间自动改变列宽度并且不可修改列宽度
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表头不可见
        self.tableView.horizontalHeader().setVisible(False)
        # 纵向表头不可见
        self.tableView.verticalHeader().setVisible(False)
        # 设置表格内容文字大小
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        # 设置表格内容不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 垂直滚动条始终开启
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)




    # 查询按钮的单击事件
    def on_click(self):
        get_from = self.textEdit.toPlainText()  # 获取出发地
        get_to = self.textEdit_2.toPlainText()  # 获取到达地
        get_date = self.textEdit_3.toPlainText()  # 获取出发时间
        # 判断车站文件是否存在
        if is_stations('stations.text') == True:
            stations = eval(read('stations.text'))  # 读取所有车站并转换为dic类型
            # 判断所有参数是否为空，出发地、目的地、出发日期
            if get_from != "" and get_to != "" and get_date != "":
                # 判断输入的车站名称是否存在，以及时间格式是否正确
                if get_from in stations and get_to in stations and self.is_valid_date(get_date):
                    # 计算时间差
                    time_difference = self.time_difference(self.get_time(), get_date).days
                    # 判断时间差为0时证明是查询当前的查票，
                    # 以及29天以后的车票。12306官方要求只能查询30天以内的车票
                    if time_difference >= 0 and time_difference <= 29:
                        from_station = stations[get_from]  # 在所有车站文件中找到对应的参数，出发地
                        to_station = stations[get_to]  # 目的地
                        data = query(get_date, from_station, to_station)  # 发送查询请求,并获取返回的信息
                        self.checkBox_default()
                        if len(data) != 0:  # 判断返回的数据是否为空
                            # 如果不是空的数据就将车票信息显示在表格中
                            self.displayTable(len(data), 16, data)
                        else:
                            messageDialog('警告', '没有返回的网络数据！')
                    else:
                        messageDialog('警告', '超出查询日期的范围内,'
                                                 '不可查询昨天的车票信息,以及29天以后的车票信息！')
                else:
                    messageDialog('警告', '输入的站名不存在,或日期格式不正确！')
            else:
                messageDialog('警告', '请填写车站名称！')
        else:
            messageDialog('警告', '未下载车站查询文件！')

    # 将所有车次分类复选框取消勾选
    def checkBox_default(self):
        self.checkBox_G.setChecked(False)
        self.checkBox_D.setChecked(False)
        self.checkBox_Z.setChecked(False)
        self.checkBox_T.setChecked(False)
        self.checkBox_K.setChecked(False)

    # 高铁复选框事件处理
    def change_G(self, state):
        # 选中将高铁信息添加到最后要显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取高铁信息
            g_vehicle()
            # 通过表格显示该车型数据
            self.displayTable(len(type_data), 16, type_data)
        else:
            # 取消选中状态将移除该数据
            r_g_vehicle()
            self.displayTable(len(type_data), 16, type_data)

    # 动车复选框事件处理
    def change_D(self, state):
        # 选中将动车信息添加到最后要显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取动车信息
            d_vehicle()
            # 通过表格显示该车型数据
            self.displayTable(len(type_data), 16, type_data)

        else:
            # 取消选中状态将移除该数据
            r_d_vehicle()
            self.displayTable(len(type_data), 16, type_data)

    # 直达复选框事件处理
    def change_Z(self, state):
        # 选中将直达车信息添加到最后要显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取直达车信息
            z_vehicle()
            self.displayTable(len(type_data), 16, type_data)
        else:
            # 取消选中状态将移除该数据
            r_z_vehicle()
            self.displayTable(len(type_data), 16, type_data)

    # 特快复选框事件处理
    def change_T(self, state):
        # 选中将特快车信息添加到最后要显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取特快车信息
            t_vehicle()
            self.displayTable(len(type_data), 16, type_data)
        else:
            # 取消选中状态将移除该数据
            r_t_vehicle()
            self.displayTable(len(type_data), 16, type_data)

    # 快速复选框事件处理
    def change_K(self, state):
        # 选中将快车信息添加到最后要显示的数据当中
        if state == QtCore.Qt.Checked:
            # 获取快速车信息
            k_vehicle()
            self.displayTable(len(type_data), 16, type_data)

        else:
            # 取消选中状态将移除该数据
            r_k_vehicle()
            self.displayTable(len(type_data), 16, type_data)



    # 显示车次信息的表格
    # train参数为共有多少趟列车，该参数作为表格的行。
    # info参数为每趟列车的具体信息，例如有座、无座卧铺等。该参数作为表格的列
    def displayTable(self, train, info, data):
        self.model.clear()
        for row in range(train):
            for column in range(info):
                # 添加表格内容
                item = QStandardItem(data[row][column])
                # 向表格存储模式中添加表格具体信息
                self.model.setItem(row, column, item)
        # 设置表格存储数据的模式
        self.tableView.setModel(self.model)

    # 获取系统当前时间并转换请求数据所需要的格式
    def get_time(self):
        # 获得当前时间时间戳
        now = int(time.time())
        # 转换为其它日期格式,如:"%Y-%m-%d %H:%M:%S"
        timeStruct = time.localtime(now)
        strTime = time.strftime("%Y-%m-%d", timeStruct)
        return strTime

    # 计算购票时间差，因为只能提前购买29天的车票
    def time_difference(self, in_time, new_time):
        # 将字符串日期转换为struct_time时间对象
        in_time = time.strptime(in_time, "%Y-%m-%d")
        new_time = time.strptime(new_time, "%Y-%m-%d")
        # 将struct_time时间对象转换为datetime对象
        in_time = datetime.datetime(in_time[0], in_time[1], in_time[2])
        new_time = datetime.datetime(new_time[0], new_time[1], new_time[2])
        # 返回两个变量相差的值，就是相差天数
        return new_time - in_time

    def is_valid_date(self, str):
        '''判断是否是一个有效的日期字符串'''
        try:
            time.strptime(str, "%Y-%m-%d")
            return True
        except:
            return False
    # 卧铺售票分析查询按钮的事件处理
    def query_ticketing_analysis_click(self):
        self.info_table = []         # 保存窗体表格中的车次信息
        today_car_list.clear()  # 清空今天列车信息，已处理是否有票
        three_car_list.clear()  # 清空三天列车信息，已处理是否有票
        five_car_list.clear()  # 清空五天列车信息，已处理是否有票
        today_list.clear()     # 清空今天列车信息，未处理是否有票
        three_list.clear()     # 清空三天列车信息，未处理是否有票
        five_list.clear()      # 清空五天列车信息，未处理是否有票
        get_from = self.textEdit_analysis_from.toPlainText() # 获取出发地
        get_to = self.textEdit_analysis_to.toPlainText() # 获取到达地
        stations = eval(read('stations.text'))  # 读取所有车站并转换为dic类型

        # 判断所有参数是否为空，出发地、目的地
        if get_from != "" and get_to != "" :
            # 判断输入的车站名称是否存在，以及时间格式是否正确
            if get_from in stations and get_to in stations :
                    from_station = stations[get_from]  # 在所有车站文件中找到对应的参数，出发地
                    to_station = stations[get_to]  # 目的地
                    today = datetime.datetime.now()  # 获取今天日期
                    three_set = datetime.timedelta(days=+2)  # 三天内偏移天数
                    five_set = datetime.timedelta(days=+4)  # 五天内偏移天数
                    three_day = (today + three_set).strftime('%Y-%m-%d') # 三天格式化后的日期
                    five_day = (today + five_set).strftime('%Y-%m-%d')   # 五天格式化后的日期
                    today = today.strftime('%Y-%m-%d')  # 今天格式化后的日期
                    # 发送查询今天卧铺票信息的网络请求,并获取返回的信息
                    query_ticketing_analysis(today, from_station, to_station,1)
                    # 发送查询三天内卧铺票信息的网络请求,并获取返回的信息
                    query_ticketing_analysis(three_day, from_station, to_station,3)
                    # 发送查询五天内卧铺票信息的网络请求,并获取返回的信息
                    query_ticketing_analysis(five_day, from_station, to_station,5)

                    info_set=set()   # 创建筛选车次集合，将相同车次进行整合，查看共有几趟列车
                    for i in today_car_list+three_car_list+five_car_list:
                        # 因为在集合中必须是字符串才能进行整合，所以将车次信息转换为字符串类型，方便车次整合
                        info_set.add(str(i[0:6]))
                    for info in info_set:             # 遍历车次信息
                        info = eval(info)              # 将车次信息再次转换成列表
                        is_today_ture = False         # 判断今天是否存在某趟列车的标记
                        for i in today_car_list:      # 遍历今天的车次信息，该车次信息是没有筛选的信息
                            if info[0] in i:          # 判断整合后的车次，在今天的车次信息中是否存在
                                is_today_ture= True   # 存在就进行标记
                                info.append(i[6])      # 如果存在就将，车次信息中是否有卧铺的信息添加至整合后的车次信息中
                                break                 # 跳出循环
                        if is_today_ture==False:      # 如果今天没有某一趟列车就标记为'--'
                            info.append('--')
                        is_three_ture = False          # 判断三天是否存在某趟列车的标记
                        for i in three_car_list:       # 遍历三天的车次信息，该车次信息是没有筛选的信息
                            if info[0] in i:           # 判断整合后的车次，在三天的车次信息中是否存在
                                is_three_ture = True    # 存在就进行标记
                                info.append(i[6])       # 如果存在就将，车次信息中是否有卧铺的信息添加至整合后的车次信息中
                                break                  # 跳出循环
                        if is_three_ture==False:      # 如果三天没有某一趟列车就标记为'--'
                            info.append('--')
                        is_five_ture = False          # 判断五天是否存在某趟列车的标记
                        for i in five_car_list:       # 遍历五天的车次信息，该车次信息是没有筛选的信息
                            if info[0] in i:          # 判断整合后的车次，在五天的车次信息中是否存在
                                is_five_ture = True    # 存在就进行标记
                                info.append(i[6])      # 如果存在就将，车次信息中是否有卧铺的信息添加至整合后的车次信息中
                                break                  # 跳出循环
                        if is_five_ture==False:      # 如果五天没有某一趟列车就标记为'--'
                            info.append('--')
                        self.info_table.append(info)         # 将最后结果添加至窗体表格的列表中

                    self.tableWidget.setRowCount(len(self.info_table))  # 设置表格行数
                    self.tableWidget.setColumnCount(9)             # 设置表格列数
                    # 设置表格内容文字大小
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    self.tableWidget.setFont(font)
                    # 根据窗体大小拉伸表格
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                    # 循环遍历最终的信息
                    for row in range(len(self.info_table)):
                        fraction = 0   # 分数，根据该分数判断列车的紧张程度
                        for column in range(9):
                            if column==6:   # 如果是某趟列车今天是无票
                                if self.info_table[row][column]=='无'or self.info_table[row][column]=='--':
                                    fraction+=3      # 计3分
                            if column==7:   # 如果是某趟列车三天内是无票
                                if self.info_table[row][column]=='无'or self.info_table[row][column]=='--':
                                    fraction+=2      # 计2分
                            if column == 8:  # 如果是某趟列车五天内是无票
                                if self.info_table[row][column] == '无'or self.info_table[row][column]=='--':
                                    fraction += 1    # 计1分

                        # 判断分数大于等于5分的车次为红色，说明该车次卧铺非常紧张
                        if fraction>=5:
                            # 定位是哪趟车次符合该条件，遍历该车次信息
                            for i in range(len(self.info_table[row])):
                                # 表格列中的信息
                                item = QtWidgets.QTableWidgetItem(self.info_table[row][i])
                                item.setBackground(QColor(255, 0, 0));  # 设置该车次背景颜色
                                self.tableWidget.setItem(row, i, item)  # 设置表格显示的内容
                        # 判断分数大于1与分数小于等于4的车次为橙色，说明该车次卧铺紧张
                        if fraction>=1 and fraction<=4:
                            for i in range(len(self.info_table[row])):
                                item = QtWidgets.QTableWidgetItem(self.info_table[row][i])
                                item.setBackground(QColor(255, 170, 0));
                                self.tableWidget.setItem(row, i, item)  # 设置表格显示的内容
                        # 判断分数等于0的车次为绿色，说明该车次卧铺不紧张
                        if fraction ==0:
                            for i in range(len(self.info_table[row])):
                                item = QtWidgets.QTableWidgetItem(self.info_table[row][i])
                                item.setBackground(QColor(85, 170, 0));
                                self.tableWidget.setItem(row, i, item)  # 设置表格显示的内容
                    self.show_broken_line()   # 显示折线图
        else:
            messageDialog('警告', '请填写车站名称！')
    # 显示卧铺车票数量折线图
    def show_broken_line(self):
        train_number_list=[]      # 保存车次
        tickets_number_list = []  # 保存今天，三天内，五天内所有车次的卧铺票数量

        # 遍历车次信息
        for train_number in self.info_table:
            number_list = []   # 临时保存车票数量
            if self.horizontalLayout.count() !=0:
                # 每次点循环删除管理器的组件
                while self.horizontalLayout.count():
                    # 获取第一个组件
                    item = self.horizontalLayout.takeAt(0)
                    # 删除组件
                    widget = item.widget()
                    widget.deleteLater()
            is_today_ture = False  # 判断今天是否存在某趟列车的标记
            for today in today_list:
                # 判断今天的车次信息中是否有该车次
                if train_number[0] in today:
                    is_today_ture = True  # 存在就进行标记
                    number = self.statistical_quantity(today[6:9]) # 调用统计车票数量的方法
                    number_list.append(number)                   # 将车票数量添加至临时列表中
                    break
            if is_today_ture == False:  # 如果今天没有某一趟列车，说明该车次无票为0
                number_list.append(0)
            is_three_ture = False  # 判断三天内是否存在某趟列车的标记
            for three_day in three_list:
                if train_number[0] in three_day:
                    is_three_ture = True  # 存在就进行标记
                    number = self.statistical_quantity(three_day[6:9])  # 调用统计车票数量的方法
                    number_list.append(number)  # 将车票数量添加至临时列表中
                    break
            if is_three_ture == False:  # 如果三天内没有某一趟列车，说明该车次无票为0
                number_list.append(0)
            is_five_ture = False  # 判断五天是否存在某趟列车的标记
            for five_day in five_list:
                if train_number[0] in five_day:
                    is_five_ture = True  # 存在就进行标记
                    number = self.statistical_quantity(five_day[6:9])  # 调用统计车票数量的方法
                    number_list.append(number)  # 将车票数量添加至临时列表中
                    break
            if is_five_ture == False:  # 如果五天内没有某一趟列车，说明该车次无票为0
                number_list.append(0)
            tickets_number_list.append(number_list)    # 添加车票数量列表
            train_number_list.append(train_number[0])  # 添加车次列表
        # 车次信息大时，添加滚动条扩大折线图高度
        if len(train_number_list)>=9:
            self.scrollAreaWidgetContents_2.setMinimumHeight(len(train_number_list) * 30)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 951,(len(train_number_list)*30)))

        # 创建画布对象
        line = PlotCanvas()
        line.broken_line(tickets_number_list,train_number_list)  # 调用折线图方法
        self.horizontalLayout.addWidget(line)    # 将折线图添加至底部水平布局当中

    # 统计车票数量
    def statistical_quantity(self,msg):
        number = 0    # 车票初始值
        for i in msg:
            if i=='有':   # 如果是有增加20个车票
                number+=20
            if i=='无'or i=='': # 如果是无或者是空就增加0个车票
                number+=0
            if i.isdigit():     # 如果是数字，就直接增加对应的数字
                number+=int(i)
        return number          # 返回计算后的车票数量











    # 车票起售时间查询按钮的事件处理
    def query_time_click(self):
        station = self.lineEdit_station.text()  # 获取需要查询的起售车站
        stations_time = eval(read('time.text'))  # 读取所有车站与起售时间并转换为dic类型
        stations = eval(read('stations.text'))  # 读取所有车站并转换为dic类型
        if station in stations_time:  # 判断要搜索的站名是否存在
            name_lit, time_list = query_time(stations.get(station))  # 查询起售车站对应的站名与起售时间
            if self.gridLayout.count() !=0:
                # 每次点循环删除管理器的控件
                while self.gridLayout.count():
                    # 获取第一个控件
                    item = self.gridLayout.takeAt(0)
                    # 删除控件
                    widget = item.widget()
                    widget.deleteLater()

            # 行数标记
            i = -1
            for n in range(len(name_lit)):
                # x 确定每行显示的个数 0，1，2,3 每行4个
                x = n % 4
                # 当x为0的时候设置换行 行数+1
                if x == 0:
                    i += 1
                # 创建布局
                self.widget = QtWidgets.QWidget()
                # 给布局命名
                self.widget.setObjectName("widget" + str(n))
                # 设置布局样式
                self.widget.setStyleSheet('QWidget#' + "widget" + str(
                    n) + "{border:2px solid rgb(175, 175, 175);background-color: rgb(255, 255, 255);}")
                # 创建个Qlabel控件用于显示图片 设置控件在QWidget中
                self.label = QtWidgets.QLabel(self.widget)
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                # 设置大小
                self.label.setGeometry(QtCore.QRect(10, 10, 210, 65))
                font = QtGui.QFont()  # 创建字体对象
                font.setPointSize(11)  # 设置字体大小
                font.setBold(True)  # 开启粗体属性
                font.setWeight(75)  # 设置文字粗细
                self.label.setFont(font)  # 设置字体
                self.label.setText(name_lit[n]+'      '+time_list[n])   # 设置显示站名与起售时间
                # 把动态创建的widegt布局添加到gridLayout中 i，x分别代表：行数以及每行的个数
                self.gridLayout.addWidget(self.widget, i, x)
            # 设置高度为动态高度根据行数确定高度 每行300
            self.scrollAreaWidgetContents.setMinimumHeight((i+1) * 100)
            # 设置网格布局控件动态高度
            self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 950, ((i+1) * 100)))
        else:
            messageDialog('警告','起售车站中没有该车站名称！')



def show_MainWindow():
    app = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    main = Main()  # 创建主窗体对象
    main.textEdit_3.setText(main.get_time())  # 出发日显示当天日期
    main.pushButton.clicked.connect(main.on_click)  # 查询按钮指定单击事件的方法
    main.checkBox_G.stateChanged.connect(main.change_G)  # 高铁选中与取消事件
    main.checkBox_D.stateChanged.connect(main.change_D)  # 动车选中与取消事件
    main.checkBox_Z.stateChanged.connect(main.change_Z)  # 直达车选中与取消事件
    main.checkBox_T.stateChanged.connect(main.change_T)  # 特快车选中与取消事件
    main.checkBox_K.stateChanged.connect(main.change_K)  # 快车选中与取消事件
    main.pushButton_time_query.clicked.connect(main.query_time_click)  # 起售时间查询按钮指定单击事件的方法
    main.pushButton_analysis_query.clicked.connect(main.query_ticketing_analysis_click)  # 卧铺售票分析查询按钮指定单击事件的方法
    main.show()  # 显示主窗体
    sys.exit(app.exec_())  # 循环中等待退出程序


if __name__ == '__main__':
    # 判断是否有车站与起售时间的文件，没有就下载
    if is_stations('stations.text') == False and is_stations('time.text')==False:
        get_station()  # 下载所有车站文件
        get_selling_time() # 下载起售时间文件
    # 判断两种文件存在时显示窗体
    if is_stations('stations.text') == True and is_stations('time.text')==True:
        show_MainWindow()  # 调用显示窗体的方法
    else:
        messageDialog('警告','车站文件或起售时间文件出现异常！')

