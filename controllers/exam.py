import this

from PyQt5.QtCore import  QTimer
from PyQt5.QtWidgets import QWidget
from sqlalchemy.orm import sessionmaker

from views.exam import Ui_Dialog

class examfrom(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.coursename=""
        self.questionnowid=0
        self.paperlist=[]
        self.inithidebutton()
        self.pushButton_4.clicked.connect(self.kaishidati)
        self.pushButton_3.clicked.connect(self.xianshidaan)
    def xianshidaan(self):

        pass
    def kaishidati(self):
        self.settimer()

        self.pushButton_3.setHidden(False)
        self.pushButton_2.setHidden(False)
        self.pushButton.setHidden(False)
        self.pushButton_4.setHidden(True)
        from controllers.utils.createpaper import createpaper
        paper=createpaper(self.coursename)
        self.paperlist=paper.createpaper()
        self.xianshitimu()
    def xianshitimu(self):
        #题目内容
        self.textBrowser.setText("asdfasfdsa")
        #题目选项答案
        # from PyQt5.QtWidgets import QCheckBox,QGridLayout,QLabel,QHBoxLayout,QVBoxLayout
        from PyQt5 import QtWidgets


        gridtalLayout = QtWidgets.QGridLayout(self.groupBox_2)
        gridtalLayout.setSpacing(10)
        from controllers.utils.displayques import createpaper
        createpaper=createpaper( self.textBrowser,"1234155")
        for i in range(7):
            checkboxname="checkbox"+str(i)
            checkbox = QtWidgets.QCheckBox(self.groupBox_2)
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20,10)

            labelname="labelname"+str(i)
            label= QtWidgets.QLabel(self.groupBox_2)
            label.setText("1啊大哥的撒vvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
            label.setObjectName(labelname)

            gridtalLayout.addWidget(checkbox,i,1)
            gridtalLayout.addWidget(label,i,2,1,200 )








    def inithidebutton(self):
        self.pushButton.hide()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
    def settimer(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 每次计时到时间时发出信号
        self.timer.start(1000)  # 设置计时间隔并启动；单位毫秒
        self.kaoshishijian=60*60
    def operate(self):
        self.kaoshishijian-=1
        fenzhong = self.kaoshishijian // 60
        miao=self.kaoshishijian%60
        timeleft="     剩余时间："+str(fenzhong)+":"+str(miao)
        self.label_2.setText(timeleft)


