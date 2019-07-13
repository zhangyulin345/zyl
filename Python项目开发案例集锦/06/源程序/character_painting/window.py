# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/window.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets   # 导入PyQt5窗体模块
# 主窗体UI类
class Ui_MainWindow(object):
    # 主窗体设置UI方法
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")       # 主窗体对象
        MainWindow.resize(1200, 600)                 # 主窗体大小
        MainWindow.setMinimumSize(QtCore.QSize(1200, 600))   # 主窗体最小，用于保持窗体大小不变
        MainWindow.setMaximumSize(QtCore.QSize(1200, 600))   # 主窗体最大，用于保持窗体大小不变
        # 主窗体Widget控件
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 显示导入图片的Label控件
        self.input_img = QtWidgets.QLabel(self.centralwidget)       # 该控件在centralwidget当中
        self.input_img.setGeometry(QtCore.QRect(28, 85, 500, 500))  # 控件显示位置与大小
        self.input_img.setText("")                                  # 为控件设置文字
        self.input_img.setScaledContents(True)                     # 自动缩放属性
        self.input_img.setAlignment(QtCore.Qt.AlignCenter)          # 居中显示
        self.input_img.setObjectName("input_img")                   # 对象名称
        # 显示字符画图片的Label控件
        self.export_img = QtWidgets.QLabel(self.centralwidget)
        self.export_img.setGeometry(QtCore.QRect(674, 85, 500, 500))
        self.export_img.setText("")
        self.export_img.setScaledContents(True)
        self.export_img.setAlignment(QtCore.Qt.AlignCenter)
        self.export_img.setObjectName("export_img")
        # 导入按钮
        self.pushButton_input = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_input.setGeometry(QtCore.QRect(550, 160, 101, 31))
        # 为按钮指定背景图片资源样式
        self.pushButton_input.setStyleSheet("background-image: url(:/png/img/import.png);")
        self.pushButton_input.setText("")
        self.pushButton_input.setObjectName("pushButton_input")
        # 输入字符的编辑框
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(550, 220, 101, 94))
        self.textEdit.setStyleSheet("color: rgb(255, 0, 0);")  # 设置文字颜色样式
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(550, 350, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        # 选择清晰度的组合框
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # 转换按钮
        self.pushButton_conversion = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_conversion.setGeometry(QtCore.QRect(550, 420, 101, 101))
        self.pushButton_conversion.setStyleSheet("background-image: url(:/png/img/conversion.png);")
        self.pushButton_conversion.setText("")
        self.pushButton_conversion.setObjectName("pushButton_conversion")
        # 显示等待动画的Label控件
        self.loding = QtWidgets.QLabel(self.centralwidget)
        self.loding.setGeometry(QtCore.QRect(550, 250, 100, 100))
        self.loding.setText("")
        self.loding.setObjectName("loding")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)                      # 调用retranslateUi方法显示窗体文字
        QtCore.QMetaObject.connectSlotsByName(MainWindow)   # 关联信号槽

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入字符！"))
        self.comboBox.setItemText(0, _translate("MainWindow", "清晰"))
        self.comboBox.setItemText(1, _translate("MainWindow", "一般"))
        self.comboBox.setItemText(2, _translate("MainWindow", "字符"))

import img_qc_rc  # 导入资源文件
