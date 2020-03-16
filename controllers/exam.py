import re
from functools import partial
from PyQt5 import QtWidgets
from PyQt5.QtCore import  QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from model.createdb import engine
from model.question import question,tempuserans
from views.exam import Ui_Dialog

class examfrom(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.coursename=""
        self.xunlianmoshi=5
        self.zhangjie = None
        self.curentusername=''
        self.questionnowid=0
        self.paperlist=[]
        self.kaoshishijian=60
        self.inithidebutton()
        self.pushButton_4.clicked.connect(self.kaishidati)
        self.pushButton.clicked.connect(self.shangyiti)
        self.pushButton_2.clicked.connect(self.xiayiti)
        self.pushButton_3.clicked.connect(self.jiaojuan)


        self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)

        self.tihaolayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.pushButton_5.clicked.connect(self.tijiaodaan)
    def shuaxingtihao(self):
        checkboxname = "tihao" + str(self.questionnowid+1)
        qlist = self.findChildren(QtWidgets.QPushButton,checkboxname)
        for i in  qlist:
           i.setStyleSheet("background-color: green")

    def tijiaodaan(self):
        #刷新题号状态

        #获取用户答案
        # for i in range(self.gridtalLayout1.count()):
        #     self.gridtalLayout1.itemAt(i).widget()
        Session = sessionmaker(bind=engine)
        session = Session()
        questionid=self.paperlist[self.questionnowid][0]
        questionres = session.query(question.questionType).filter(
            and_(question.id ==questionid , question.course_name == self.coursename)).first()

        session.query(tempuserans).filter(tempuserans.question_id ==questionid).delete()
        tempuseran = tempuserans()
        userdaan = ""
        if questionres.questionType == 'xz':

            qlist = self.findChildren(QtWidgets.QRadioButton)
            tempkey=['A','B','C','D','E','F']
            num=0
            for i in qlist:
                name=i.isChecked()
                if name:
                    userdaan+=tempkey[int(num)]
                num+=1
            tempuseran.question_id=questionid
            tempuseran.userans=userdaan

        elif questionres.questionType == 'pd':

            qlist = self.findChildren(QtWidgets.QRadioButton)
            tempkey = ['True', 'False']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1
            tempuseran.question_id =questionid
            tempuseran.userans = userdaan

        elif questionres.questionType == 'mxz':

            qlist = self.findChildren(QtWidgets.QCheckBox)
            tempkey=['A','B','C','D','E','F']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1
            tempuseran.question_id =questionid
            tempuseran.userans = userdaan

        elif questionres.questionType == 'jd':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan=i.toPlainText()
            tempuseran.question_id =questionid
            tempuseran.userans = userdaan
        elif questionres.questionType == 'tk':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan = i.toPlainText()
            tempuseran.question_id = questionid
            tempuseran.userans = userdaan
        session.add(tempuseran)
        session.commit()
        session.close()
        if userdaan:
            self.shuaxingtihao()
        # self.xiayiti()



    def inittihaodisplay(self):
        papernum = len(self.paperlist)
        rownum = papernum // 25 + 1
        clonum = 25
        tihao=1
        for i in range(rownum):
            for j in range(clonum):
                if tihao > papernum:
                    break
                checkboxname = "tihao" + str(tihao)
                checkbox = QtWidgets.QPushButton()
                CommonUtil.set_button_style4(checkbox)
                checkbox.setFixedSize(60, 25)
                checkbox.setObjectName(checkboxname)
                checkbox.setText(str(tihao))
                self.tihaolayout.addWidget(checkbox, i,j)

                checkbox.clicked.connect(partial(self.jumptihao, checkbox.text()))
                tihao += 1

    def jumptihao(self,buttext):
        self.questionnowid=int(buttext)-1
        self.xianshitimu()
    def xianshidaan(self):

        pass
    def shangyiti(self):
        self.questionnowid-=1
        self.xianshitimu()

    def xiayiti(self):
        self.questionnowid+=1
        self.xianshitimu()
    def jiaojuan(self):
        reply = QtWidgets.QMessageBox.question(self,
                                               '交卷',
                                               "是否要交卷？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.pushButton_3.setHidden(True)
            # self.xianshitimu()
            self.close()
            from controllers.jiaojuan import juaojuan
            self.juaojuan = juaojuan(self.paperlist,self.coursename,self.curentusername,self.xunlianmoshi)

            self.juaojuan.show()

        else:
            pass

    def kaishidati(self):
        self.settimer()
        self.pushButton_3.setHidden(False)
        self.pushButton_2.setHidden(False)
        self.pushButton.setHidden(False)
        self.pushButton_4.setHidden(True)
        from controllers.utils.createpaper import createpaper
        paper=createpaper(self.coursename,self.zhangjie)
        try:
             self.paperlist=paper.createpaper()
             if len( self.paperlist)<=1:
                 QMessageBox.information(self, '考试', '出题失败')
                 self.close()
        except:
            QMessageBox.information(self, '考试', '出题失败')
        if self.paperlist:
            self.kaoshishijian=self.paperlist[-1]*60
            self.paperlist.pop()
            self.xianshitimu()
            self.inittihaodisplay()
        else:
            QMessageBox.information(self, '考试', '出题失败,请修改试卷设置')
            self.close()

    def xianshitimu(self):
        #题目内容
        from controllers.utils.displayques import displayques
        papernum=len(self.paperlist)
        questionid=0
        try:
            if self.questionnowid<papernum and self.questionnowid>=0:
                questionid=self.paperlist[self.questionnowid][0]
            else:
                questionid = self.paperlist[0][0]
        except:
            pass

        if self.questionnowid>0 and self.questionnowid<papernum-1:
            display=displayques(self,self.textBrowser,self.gridtalLayout1,questionid,self.coursename,self.questionnowid,papernum,self.tihaolayout)
            display.display()
            self.pushButton.setHidden(False)
            self.pushButton_2.setHidden(False)
            self.pushButton_5.setHidden(False)
        elif self.questionnowid==0:
            self.pushButton.setHidden(True)
            display=displayques(self,self.textBrowser,self.gridtalLayout1,questionid,self.coursename,self.questionnowid,papernum,self.tihaolayout)
            display.display()
            self.pushButton_5.setHidden(False)
        elif self.questionnowid==papernum-1:
            self.pushButton_2.setHidden(True)

            display = displayques(self,self.textBrowser, self.gridtalLayout1, questionid,self.coursename,self.questionnowid,papernum,self.tihaolayout)
            display.display()
        elif self.questionnowid<0:
            self.pushButton.setHidden(True)
            self.pushButton_5.setHidden(True)
        elif self.questionnowid>papernum-1:
            self.pushButton_2.setHidden(True)
            self.pushButton_5.setHidden(True)










    def inithidebutton(self):
        CommonUtil.set_button_style3(self.pushButton)
        CommonUtil.set_button_style3(self.pushButton_2)
        CommonUtil.set_button_style3(self.pushButton_3)
        CommonUtil.set_button_style3(self.pushButton_4)
        CommonUtil.set_button_style3(self.pushButton_5)
        self.pushButton.hide()
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_5.hide()
    def settimer(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 每次计时到时间时发出信号
        self.timer.start(1000)  # 设置计时间隔并启动；单位毫秒

    def operate(self):
        self.kaoshishijian-=1
        fenzhong = self.kaoshishijian // 60
        miao=self.kaoshishijian%60
        timeleft="     剩余时间："+str(fenzhong)+":"+str(miao)
        if self.kaoshishijian<1:
            from controllers.jiaojuan import juaojuan
            self.juaojuan = juaojuan(self.paperlist, self.coursename)

            self.juaojuan.show()
            self.close()
            self.timer.timeout.disconnect()

        self.label_2.setText(timeleft)
    # def closeEvent(self, event):
    #     """
    #     重写closeEvent方法，实现dialog窗体关闭时执行一些代码
    #     :param event: close()触发的事件
    #     :return: None
    #     """
    #     pass
    #     # self.inittempuser()


