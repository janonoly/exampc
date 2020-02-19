import this

from PyQt5.QtCore import  QTimer
from PyQt5.QtWidgets import QWidget
from sqlalchemy.orm import sessionmaker

from views.exam import Ui_Dialog

class examfrom(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        # ui=examfrom()
        # ui.show()
        # self.

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


