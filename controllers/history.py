import datetime

from PyQt5 import QtCore
from PyQt5.QtChart import QChartView, QLineSeries, QValueAxis, QChart, QCategoryAxis
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QIcon, QBrush, QPainter, QColor, QCursor, QFont
from PyQt5.QtWidgets import QWidget, QToolTip, QApplication, QStyle, QMessageBox
from controllers.utils.modeutil import ModelUtil


from controllers.utils.loginutil import CommonUtil
from views.history import Ui_Dialog

class Historyfrom(QWidget,Ui_Dialog):
    def __init__(self,username):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.username=username
        try:
            self.create_chart()
        except:
            QMessageBox.information(self, '提示', '没有历史成绩')



    def create_chart(self):
        # 创建折线视图窗口
        modelutil = ModelUtil()

        dataTable = modelutil.get_score(self.username)


        chart = QChartView(self)
        #获取显示器高宽
        screeRect=QApplication.desktop().screenGeometry()
        height=screeRect.height()*4/5
        whidth = screeRect.width()*9/10
        padding=screeRect.width()*1/20
        chart.setGeometry(
            QtCore.QRect(padding,10,whidth,height))
        chart.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        chart.raise_()


        # qfont=QFont()
        # qfont.setPointSize(34)
        # qfont.setPixelSize(45)

        chart._chart = QChart(title="考试成绩折线图")  # 创建折线视图
        # chart._chart.setFont(qfont)
        # chart.setStyleSheet(
        #                          "QChartView{border:2px}"
        #                          "QChartView{border-radius:10px}"
        #                          "QChartView{font-family:宋体}"
        #                          "QChartView{word-wrap:true}"
        #                          "QChartView{font-size:25px}"
        #                          "QChartView{padding:2px 2px}")
        # chart._chart.setFont(qfont)
        # chart._chart.setBackgroundVisible(visible=False)      # 背景色透明
        chart._chart.setBackgroundBrush(QBrush(QColor("#FFFFFF")))  # 改变图背景色

        #  图形项默认无法接收悬停事件，可以使用QGraphicsItem的setAcceptHoverEvents()函数使图形项可以接收悬停事件。
        chart._chart.setAcceptHoverEvents(True)
        # 4条折线的坐标值


        # 执行创建折线的函数
        self.create_series(dataTable, chart)

        chart._chart.createDefaultAxes()  # 创建默认的轴

        chart._chart.axisY().setTickCount(11)  # y1轴设置10个刻度
        chart._chart.axisY().setLabelFormat("%d")
        chart._chart.axisY().setRange(0, 100)  # 设置y1轴范围

        xnum=len(dataTable[0])-1
        chart._chart.axisX().setTickCount(xnum)  # X轴设置10个刻度
        # 执行定义X轴的函数
        # self.customAxisX(chart._chart)

        chart.setChart(chart._chart)

    def create_series(self, dataTable, chart):
        # 创建折线的函数
        for i, data_list in enumerate(dataTable):  # [index,[list]]
            # 创建曲线
            series = QLineSeries(chart._chart)
            # 设置折线名
            series.setName(data_list[0])

            for j, v in enumerate(data_list[1:]):
                #  添加折线和对应的坐标点
                series.append(j, v)

            series.setPointsVisible(True)  # 显示原点
            # 鼠标悬停连接事件
            series.hovered.connect(self.onSeriesHoverd)
            chart._chart.addSeries(series)  # 添加折线到视图窗口
        return chart._chart

    def customAxisX(self, chart):
        # 自定义x轴(均分)
        chart = chart
        series = chart.series()
        if not series:
            return
        # 获取当前时间前8小时的一小时内的时间
        time = []
        for index in range(13):
            num = 60 / 13
            last_day = (datetime.datetime.now() + datetime.timedelta(hours=-8, minutes=- index * num)).strftime(
                "%H:%M")
            time.append(last_day)
        category = list(reversed(time))

        '''QValueAxis是轴的范围什么的不需要自己指定，轴上显示的label（也就是0,1,2,3这些内容）是默认的。
        qt会根据你轴上的点自动设置。若你需要自定义一些内容，QCategoryAxis是比较好的，但是需要自己自定义好才可以调用。'''
        axisx = QCategoryAxis(
            chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)

        axisx.setGridLineVisible(False)  # 隐藏网格线条
        axisx.setTickCount(len(category))  # 设置刻度个数
        minx = chart.axisX().min()
        maxx = chart.axisX().max()
        tickc = chart.axisX().tickCount()
        print(tickc)
        if tickc < 2:
            axisx.append(category[0])
        else:
            step = (maxx - minx) / (tickc - 1)  # tickc>=2
            for i in range(0, tickc):
                axisx.append(category[i], minx + i * step)
                # 保存x轴值
        chart.setAxisX(axisx, series[-1])

    def onSeriesHoverd(self, point, state):
        # 鼠标悬停事件(底部x,y)
        if state:
            try:
                name = self.sender().name()
            except:
                # QCursor.pos()悬停提示文字显示的位置
                name = ""
            QToolTip.showText(QCursor.pos(), "%s\nx: %s\ny: %s" %
                              (name, round(point.x(),1), round(point.y(),1)))
