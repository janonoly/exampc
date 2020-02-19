import this

from PyQt5 import QtWidgets
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
        self.kaoshishijian=60
        self.inithidebutton()
        self.pushButton_4.clicked.connect(self.kaishidati)
        self.pushButton.clicked.connect(self.shangyiti)
        self.pushButton_2.clicked.connect(self.xiayiti)
        self.pushButton_3.clicked.connect(self.jiaojuan)

        self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)




    def xianshidaan(self):

        pass
    def shangyiti(self):
        self.questionnowid-=1
        self.xianshitimu()
    def xiayiti(self):
        self.questionnowid+=1
        self.xianshitimu()
    def jiaojuan(self):
        self.pushButton_3.setHidden(True)
        # self.xianshitimu()
    def kaishidati(self):
        self.settimer()
        self.pushButton_3.setHidden(False)
        self.pushButton_2.setHidden(False)
        self.pushButton.setHidden(False)
        self.pushButton_4.setHidden(True)
        from controllers.utils.createpaper import createpaper
        paper=createpaper(self.coursename)
        self.paperlist=paper.createpaper()
        self.kaoshishijian=self.paperlist[-1]*60
        self.paperlist.pop()
        self.xianshitimu()
    def xianshitimu(self):
        #题目内容
        from controllers.utils.displayques import displayques
        papernum=len(self.paperlist)
        questionid=0
        try:
            if self.questionnowid<20 and self.questionnowid>=0:
                questionid=self.paperlist[self.questionnowid][0]
            else:
                questionid = self.paperlist[0][0]
        except:
            pass

        if self.questionnowid>0 and self.questionnowid<papernum:
            display=displayques(self,self.textBrowser,self.gridtalLayout1,questionid,self.coursename)
            display.display()
            self.pushButton.setHidden(False)
            self.pushButton_2.setHidden(False)
        elif self.questionnowid==0:
            self.pushButton.setHidden(True)
            display=displayques(self,self.textBrowser,self.gridtalLayout1,questionid,self.coursename)
            display.display()
        elif self.questionnowid==papernum:
            self.pushButton_2.setHidden(True)
            display = displayques(self,self.textBrowser, self.gridtalLayout1, questionid,self.coursename)
            display.display()
        elif self.questionnowid<0:
            self.pushButton.setHidden(True)
        elif self.questionnowid>papernum:
            self.pushButton_2.setHidden(True)










    def inithidebutton(self):
        self.pushButton.hide()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
    def settimer(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 每次计时到时间时发出信号
        self.timer.start(1000)  # 设置计时间隔并启动；单位毫秒

    def operate(self):
        self.kaoshishijian-=1
        fenzhong = self.kaoshishijian // 60
        miao=self.kaoshishijian%60
        timeleft="     剩余时间："+str(fenzhong)+":"+str(miao)
        self.label_2.setText(timeleft)


