
from window import Ui_MainWindow  # 导入主窗体UI类
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog  # 导入qt窗体类
from PyQt5 import QtGui
import sys  # 导入系统模块
import _thread  # 导入线程模块
import time     # 导入时间模块

import conversion  # 导入用于转换的模块

# 主窗体初始化类
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        # 开启自动填充背景
        self.centralwidget.setAutoFillBackground(True)
        palette = QtGui.QPalette()  # 调色板类
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(
            QtGui.QPixmap('img/bg.png')))  # 设置背景图片
        self.centralwidget.setPalette(palette)  # 设置调色板

        input_img = QtGui.QPixmap('img/input_test.png')  # 打开位图
        self.input_img.setPixmap(input_img)  # 设置位图

        export_img = QtGui.QPixmap('img/output_test.png')  # 打开位图
        self.export_img.setPixmap(export_img)  # 设置位图

    # 打开图片文件路径
    def openfile(self):
        # 打开文件的窗体，进行图片的选择
        openfile_name = QFileDialog.getOpenFileName()
        if openfile_name[0] != '':
            self.input_path = openfile_name[0]   # 获取选中的图片路径
            self.show_input_img(self.input_path) # 调用显示导入图片的方法

    # 显示导入的图片
    def show_input_img(self,file_path):
        input_img = QtGui.QPixmap(file_path)  # 打开位图
        self.input_img.setPixmap(input_img)  # 设置位图

    # 启动转换图片
    def start_conversion(self):
        if hasattr(main,'input_path'):
            self.gif = QtGui.QMovie('img\loding.gif')  # 加载gif图片
            self.loding.setMovie(self.gif)  # 设置gif图片
            self.gif.start()  # 启动图片，实现等待gif图片的显示
            # 线程启动转换方法，避免与主窗体冲突
            _thread.start_new_thread(lambda: self.is_conversion(main.input_path),())
        else:
            print('没有选择指定的图片路径！')


    # 转换方法，方便线程启动
    def is_conversion(self, file_path):
        t = str(int(time.time()))  # 当前时间戳,秒级
        # 转换后的字符画图片路径
        export_path = 'export_img\\export_img'+t+'.png'
        input_char = main.textEdit.toPlainText()  # 获取输入的字符内容
        definition =main.comboBox.currentText()   # 获取选中的文字
        # 调用转换字符画的方法file_path为输入图片路径，
        is_over = conversion.picture_conversion(file_path,export_path,input_char,definition)
        if is_over == False:  # 判断图片是否转换完毕
            self.loding.clear()   # 转换完毕就将等待gif图片清理掉
            main.show_export_img(export_path)  # 调用显示转换后的字符换图片方法


    # 显示转换后的字符画图片
    def show_export_img(self,file_path):
        export_img = QtGui.QPixmap(file_path)  # 打开位图
        self.export_img.setPixmap(export_img)  # 设置位图



if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建GUI对象
    main = Main()  # 创建主窗体ui类对象
    main.show()  # 显示主窗体

    main.pushButton_input.clicked.connect(main.openfile)  # 导入文件按钮指定打开图片文件路径的事件
    main.pushButton_conversion.clicked.connect(main.start_conversion) # 转换按钮指定启动转换图片的方法
    sys.exit(app.exec_())  # 除非退出程序关闭窗体，否则一直运行
