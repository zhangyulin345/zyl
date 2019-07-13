import sys  # 操作系统模块
from PyQt5.QtGui import  QColor  # 导入PyQt5的QtGui模块
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTableWidget, QMessageBox # 导入PyQt5的QtWidgets模块
import os  # 导入操作系统模块
import tools.common as common  # 导入工具模块并设置别名为common
import tools.wordtopdf as wordtopdf
import tools.mergepdf as mergepdf
from mainWindow import *   # 导入主窗体的UI类
from pageWindow import *  # 导入Word转PDF窗体的UI类
from listWindow import *  # 导入统计Word文档页码窗体的UI类
from transformWindow import *  # 导入提取总页码窗体的UI类
import _thread
# 主窗体初始化类
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow,self).__init__()
        self.setupUi(self)
        self.setGeometry(100, 100, 1024, 600)
        self.setWindowTitle('Word助手')  # 设置窗体的标题
        # 设置窗体背景
        palette = QtGui.QPalette()  # 创建调色板类的对象
        # 设置窗体背景自适应
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap("./image/bg.png").scaled(self.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)
        self.setAutoFillBackground(True) # 设置自动填充背景
        self.setFixedSize(1024,600)  # 禁止显示最大化按钮及调整窗体大小


'''Word转PDF模块'''
class TransformWindow(QMainWindow, Ui_TransformWindow):
    filelist = []
    def __init__(self):
        super(TransformWindow,self).__init__()
        self.setupUi(self)
        self.showLoding.setText("")  # 设置显示转换进度标签不显示内容
        self.showLoding.setMinimumWidth(100)  # 设置Label标签的最小宽度

        self.multipleExecute.clicked.connect( self.multipleExecuteClick)  #批量转换按钮绑定槽函数
        self.singleExecute.clicked.connect(self.singleExecuteClick)  # 合为一个PDF按钮绑定槽函数
        self.sourcebrowseButton.clicked.connect(self.sourcebrowseClick)   # 选择源文件夹按钮绑定槽函数
        self.targetbrowseButton.clicked.connect(self.targetbrowseClick)   # 选择目标文件夹按钮绑定槽函数
        self.listpdf.itemDoubleClicked.connect(self.itemdoubleClick)  # 为列表项的双击事件绑定槽函数
    # 自定义打开子窗体的方法
    def open(self):
        self.__init__()
        self.show()  # 显示子窗体
    def sourcebrowseClick(self):  # 单击浏览源文件夹按钮所触发的方法
        # 打开选择文件夹的对话框
        dir_path = QFileDialog.getExistingDirectory(self, "请选择源文件目录", r"E:\learn\test\doc")
        if dir_path == "":  # 处理没有选择路径的情况，这里为直接返回
            return
        self.sourcepath.setText(dir_path)  # 将获取到的文件夹路径添加到文本框控件中
        self.listword.clear()   # 清空列表
        global filelist  # 定义全局变量
        filelist = common.getfilenames(dir_path,[],'.doc')  # 获取Word文档路径
        self.listword.addItems(filelist)  # 将获取到的Word文件路径添加到列表控件中

    def targetbrowseClick(self): # 单击浏览目标文件夹按钮所触发的方法
        dir_path = QFileDialog.getExistingDirectory(self, "请选择目标文件目录", r"E:\learn\test\pdf")
        self.targetpath.setText(dir_path)

    def itemdoubleClick(self,item):  # 处理双击列表项触发的方法
        if os.path.exists(item.text()):
            os.startfile(item.text())  # 打开文件
        else:
            QMessageBox.information(self, "温馨提示：", "不是有效的文件名！", QMessageBox.Yes)

    def multipleExecuteClick(self):  #批量转换按钮触发的方法
        # 判断是否选择了源文件，如果没有选择则弹出提示框告知
        if self.listword.count() == 0:
            QMessageBox.information(self, "温馨提示：", "没有要转换的Word文档！", QMessageBox.Yes)
            return
        targetpath = self.targetpath.text()  # 获取目标文件夹
        # 判断是否选择了目标文件，如果没有选择则弹出提示框告知
        if not os.path.exists(targetpath):
            QMessageBox.information(self, "温馨提示：", "请选择正确的目标路径！", QMessageBox.Yes)
            return
        self.listpdf.clear()  # 清空结果列表
        self.showLoding.setMovie(self.gif)  # 设置gif图片
        self.gif.start()  # 启动图片，实现等待gif图片的显示
        _thread.start_new_thread(self.mExecute, ())  # 开启新线程执行批量转PDF

    # 实现批量Word转PDF操作的方法
    def mExecute(self):
        targetpath = self.targetpath.text()  # 获取目标文件夹
        valueList = wordtopdf.wordtopdf(filelist,targetpath)  # 实现将Word文档批量转换为PDF
        if(valueList != -1):
            self.showLoding.clear()  # 清除进度条
            self.listpdf.addItems(valueList)  # 将转换后的PDF路径显示在目标列表中

    # 合为一个PDF按钮所触发的方法
    def singleExecuteClick(self):
        # 判断是否选择了源文件，如果没有选择则弹出提示框告知
        if self.listword.count() == 0:
            QMessageBox.information(self, "温馨提示：", "没有要转换的Word文档！", QMessageBox.Yes)
            return
        # 判断是否选择了目标文件夹，如果没有选择则弹出提示框告知
        if not os.path.exists(self.targetpath.text()):
            QMessageBox.information(self, "温馨提示：", "请选择正确的目标路径！", QMessageBox.Yes)
            return
        self.listpdf.clear()  # 清空结果列表
        self.showLoding.setMovie(self.gif)  # 设置gif图片
        self.gif.start()  # 启动图片，实现等待gif图片的显示
        _thread.start_new_thread(self.sExecute,())  # 开启新线程执行多个Word合为一个PDF

    # 实现合为一个PDF文件操作的方法
    def sExecute(self):
        targetpath = self.targetpath.text()  # 获取目标路径
        valueList = wordtopdf.wordtopdf(filelist, targetpath)  # 将多个Word文档转换为PDF文件
        if(valueList != -1):
            mergepdf.mergefiles(targetpath, 'merged.pdf', True) # 将多个PDF文件合并为一个PDF文件
            self.showLoding.clear()  # 清除进度条
            temp = [os.path.join(targetpath , 'merged.pdf')] # 组合PDF文件路径
            self.listpdf.addItems( temp)  # 将PDF文件路径显示到结果列表中
            for file in valueList: # 遍历临时生成的PDF文件列表
                os.remove(file)  # 删除PDF文件

'''统计Word文档页码模块'''
class PageWindow(QMainWindow, Ui_PageWindow):

    filelist = []    # Word文件路径列表
    def __init__(self):
        super(PageWindow,self).__init__()
        self.setupUi(self)
        self.pagetable.setColumnWidth(0,600)  # 设置第一列的宽度
        self.pagetable.setColumnWidth(1,100)  # 设置第二列的宽度
        self.pagetable.setStyleSheet("background-color: lightblue"
                                     "(spread:pad,stop:0.823 rgba(255, 255, 255, 204), stop:1 rgba(255, 255, 255, 204));"
                                     "selection-background-color:lightblue;")
        headItem = self.pagetable.horizontalHeaderItem(0)  # 获得水平方向表头的Item对象
        headItem.setBackground(QColor(0, 60, 10))  # 设置单元格背景颜色
        headItem.setForeground(QColor(200, 111, 30))  # 设置文字颜色
        headItem = self.pagetable.horizontalHeaderItem(1)  # 获得水平方向表头的Item对象
        headItem.setBackground(QColor(0, 60, 10))  # 设置单元格背景颜色
        headItem.setForeground(QColor(200, 111, 30))  # 设置文字颜色
        self.pagetable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pagetable.setSelectionBehavior(QTableWidget.SelectRows)
        self.pagetable.setSelectionMode(QTableWidget.SingleSelection)
        self.pagetable.setAlternatingRowColors(True)
        self.totalpage.setMinimumWidth(100)  # 设置Label标签的最小宽度

        self.browseButton.clicked.connect(self.sourcebrowseClick)  # 选择源路径
        self.executeButton.clicked.connect(self.executeClick)  # 开始统计按钮的事件绑定

    # 自定义打开子窗体的方法
    def open(self):
        self.__init__()
        self.show()  # 显示子窗体


    def sourcebrowseClick(self):
        dir_path = QFileDialog.getExistingDirectory(self, "请选择源文件目录", r"E:\learn\test\doc")
        if dir_path != "":  # 判断已经选择了源文件目录
            self.sourcepath.setText(dir_path)
            self.listword.clear()   # 清空列表
            global filelist
            filelist = common.getfilenames(dir_path,[],'.doc')  # 获取Word文档
            self.listword.addItems(filelist)

    def executeClick(self):  #开始统计按钮的自定义事件
        if self.listword.count() == 0:
            QMessageBox.information(self, "温馨提示：", "没有要统计页码的Word文档！", QMessageBox.Yes)
            return
        self.totalpage.setText("")
        self.totalpage.setMovie(self.gif)  # 设置gif图片
        self.label_2.setText("正在统计：")
        self.gif.start()  # 启动图片，实现等待gif图片的显示
        _thread.start_new_thread(self.execute,())  # 开启新线程执行统计页码
    # 统计页码
    def execute(self):
        valueList = []
        valueList = wordtopdf.wordtopdf1(filelist)
        # if valueList != []:
        #     self.totalpage.clear()  # 转换完毕就将等待gif图片清理掉
        totalPages = str(valueList[0]) # 总页数
        self.label_2.setText("合计页码：")
        self.totalpage.setText(totalPages)   # 显示统计出来的页码
        print("行数：",len(valueList[1]))
        self.pagetable.setRowCount(len(valueList[1]))  # 指定行数
        resultList = valueList[1]  # 获取统计结果
        for i in range(self.pagetable.rowCount()):
            for j in range(self.pagetable.columnCount()):
                content = resultList[i][j]  # 获取一个单元格的内容
                newItem = QTableWidgetItem(content)  # 转换为一个单元格对象
                self.pagetable.setItem(i, j, newItem)  # 显示在单元格中

'''提取总目录模块'''
class ListWindow(QMainWindow, Ui_ListWindow):
    def __init__(self):
        super(ListWindow,self).__init__()
        self.setupUi(self)
        self.browseButton.clicked.connect(self.sourcebrowseClick)   # 选择源路径
        self.executeButton.clicked.connect( self.getListClick)  #按钮事件绑定
        self.openButton.clicked.connect(self.openButtonClick)  # 为打开文件按钮绑定事件
    # 自定义打开子窗体的方法
    def open(self):
        self.__init__()
        self.show()  # 显示子窗体
    def sourcebrowseClick(self):
        dir_path = QFileDialog.getExistingDirectory(self, "请选择源文件目录", r"E:\learn\test\doc")
        if dir_path != "":  # 判断已经选择了源文件目录
            self.sourcepath.setText(dir_path)
            self.listword.clear()   # 清空列表
            global filelist
            filelist = common.getfilenames(dir_path,[],'.doc')  # 获取Word文档
            self.listword.addItems(filelist)

    def getListClick(self):  #子窗体自定义事件
        if self.listword.count() == 0:
            QMessageBox.information(self, "温馨提示：", "没有要提取目录的Word文档！", QMessageBox.Yes)
            return
        self.listfile.setText("")
        self.listfile.setMovie(self.gif)  # 设置gif图片
        self.gif.start()  # 启动图片，实现等待gif图片的显示
        _thread.start_new_thread(self.getList,())  # 开启新线程执行统计页码

     # 提取目录
    def getList(self):
        sourcepath = self. sourcepath.text()  # 获取源路径
        if not os.path.exists(sourcepath):  # 判断是否选择了源目录
            QMessageBox.information(self,"温馨提示：","请先选择Word文档所在的文件夹！",QMessageBox.Yes)
            return
        targetpath = os.path.join(sourcepath, "pdf")  # 根据源路径生成目标目录
        if not os.path.exists(targetpath):  # 判断目录是否存在，不存在则创建
            os.makedirs(targetpath) # 创建目录
        valueList = wordtopdf.wordtopdf(filelist, targetpath)
        if(valueList != -1):
            mergepdf.mergefiles(targetpath, 'merged.pdf', True)  # 合并PDF
            temp = [os.path.join(targetpath , 'merged.pdf')] # 生成合并后的PDF文件的路径
            for file in valueList: # 遍历临时生成的PDF文件列表
                os.remove(file)  # 删除PDF文件
            isList = self.checkBox.isChecked()    # 指定是否带目录
            resultvalue=wordtopdf.getPdfOutlines(temp[0],targetpath,isList)   # 提取目录
            os.remove(temp[0]) # 删除合并后的PDF文件
            if valueList != []:
                self.listfile.clear()  # 转换完毕就将等待gif图片清理掉
            self.listfile.setText(resultvalue)  # 将生成的目录文件路径显示到页面中


    # 自定义打开子窗体的方法
    def open(self):
        self.__init__()
        self.show()  # 显示子窗体

    # 打开文件按钮触发的事件函数
    def openButtonClick(self):
        if self.listfile.text() == "还未提取...":
            QMessageBox.information(self,"温馨提示：","还没有提取目录，请先单击【开始提取】按钮！",QMessageBox.Yes)
        else:
            os.startfile(self.listfile.text())  # 打开文件

if __name__ == '__main__':
    app = QApplication(sys.argv)   # 创建GUI对象
    main = MyMainWindow()   # 创建主窗体ui类对象
    qmovie = QtGui.QMovie('image/loding.gif')

    transformWindow = TransformWindow()  # 创建Word转PDF窗体对象
    transformWindow.gif = qmovie  # 加载gif图片
    main.actionWord_PDF.triggered.connect(transformWindow.open)  #为Toolbar上的Word转PDF按钮指定连接槽函数

    pagewindow = PageWindow()  # 创建统计Word文档页码窗体对象
    pagewindow.gif = qmovie  # 加载gif图片
    main.action_Word.triggered.connect(pagewindow.open)  #为Toolbar上的统计Word文档页码按钮指定连接槽函数

    listwindow = ListWindow()  # 创建提取总目录窗体对象
    listwindow.gif = qmovie  # 加载gif图片
    main.action_list.triggered.connect(listwindow.open)  #为Toolbar上的提取总目录按钮指定连接槽函数

    main.show()  # 显示主窗体
    sys.exit(app.exec_())   # 除非退出程序关闭窗体，否则一直运行


