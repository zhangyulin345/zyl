# 图形画布
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib  # 导入图表模块
import matplotlib.pyplot as plt # 导入绘图模块


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=0, height=0, dpi=100):
        # 避免中文乱码
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 创建图形
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        # 初始化图形画布
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)  # 设置父类

    # 折线图
    def broken_line(self,number,train_list):
        '''
        linewidth:折线的宽度
        marker：折点的形状
        markerfacecolor：折点实心颜色
        markersize：折点大小
        '''
        day_x = ['今天', '三天内', '五天内']  # X轴折线点
        for index, n in enumerate(number):
            plt.plot(day_x, n, linewidth=1, marker='o',
                     markerfacecolor='blue', markersize=8, label=train_list[index])  # 绘制折线
        plt.legend(bbox_to_anchor=(-0.03,1))  # 让图例生效，并设置图例显示位置
        plt.title('卧铺车票数量走势图')  # 标题名称