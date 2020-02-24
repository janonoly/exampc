from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from model.createdb import engine
from model.question import question,tempuserans
from views.train import Ui_Dialog

class trainfrom(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.coursename=""
        self.zhangjie=None
        self.questionnowid=0
        self.pushButton.clicked.connect(self.shangyiti)
        self.pushButton_2.clicked.connect(self.xiayiti)
        self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)
        self.pushButton_5.clicked.connect(self.tijiaodaan)
        # self.lineEdit.textChanged.connect(self.changtihao1)
        self.pushButton_3.clicked.connect(self.inittimu)
        self.tihaolayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.initbutton()

    def initbutton(self):
        self.pushButton_2.setHidden(True)
        self.pushButton_5.setHidden(True)
        self.pushButton.setHidden(True)

    def inittimu(self):
        self.pushButton_3.setHidden(True)
        self.pushButton_2.setHidden(False)
        self.pushButton_5.setHidden(False)
        self.pushButton.setHidden(True)
        # 按章节训练
        Session = sessionmaker(bind=engine)
        session = Session()
        if self.zhangjie:
            self.questionresall = session.query(question.id).filter(
            and_(question.zhangjie == self.zhangjie, question.course_name == self.coursename)).all()
            self.inittihaodisplay()
        else:
            # 不按章节训练
            self.questionresall = session.query(question.id).filter(
            and_(question.course_name == self.coursename)).all()
            self.groupBox_3.setHidden(True)
        self.xianshitimu()
        self.label.setText('共'+str(len(self.questionresall))+'题')


    # def changtihao1(self):
    #     try:
    #         self.questionnowid = int(self.lineEdit.text())
    #     except:
    #         pass
    def tijiaodaan(self):

        Session = sessionmaker(bind=engine)
        session = Session()
        questionid=self.questionresall[0].id
        if self.questionnowid<len(self.questionresall):
            questionid= self.questionresall[self.questionnowid].id
        questionres = session.query(question).filter(
            and_(question.id ==questionid , question.course_name == self.coursename)).first()

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


        elif questionres.questionType == 'pd':

            qlist = self.findChildren(QtWidgets.QRadioButton)
            tempkey = ['True', 'False']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1


        elif questionres.questionType == 'mxz':

            qlist = self.findChildren(QtWidgets.QCheckBox)
            tempkey=['A','B','C','D','E','F']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1


        elif questionres.questionType == 'jd':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan=i.toPlainText()

        anser=questionres.answer

        self.label_2.setText("正确答案为："+anser+"   我的答案："+userdaan)
        session.close()
        if userdaan:
            self.shuaxingtihao()

    def shuaxingtihao(self):
        checkboxname = "tihao" + str(self.questionnowid+1)
        qlist = self.findChildren(QtWidgets.QPushButton,checkboxname)
        for i in  qlist:
           i.setStyleSheet("background-color: green")

    def shangyiti(self):
        self.questionnowid-=1

        # self.changetihao()
        self.xianshitimu()
        self.label_2.setText('')
        if self.questionnowid <= len(self.questionresall) - 1:
            self.pushButton_2.setHidden(False)
        if self.questionnowid <= 0:
            self.pushButton.setHidden(True)

    def xiayiti(self):
        self.questionnowid += 1
        # self.changetihao()
        self.xianshitimu()
        self.label_2.setText('')

        if self.questionnowid >= len(self.questionresall)-1:
            self.pushButton_2.setHidden(True)
        if self.questionnowid > 0:
            self.pushButton.setHidden(False)


    def xianshitimu(self):
        #题目内容
        from controllers.utils.displayques import displayques
        questionid = self.questionresall[self.questionnowid].id
        papernum=len(self.questionresall)
        display = displayques(self,self.textBrowser, self.gridtalLayout1, questionid,self.coursename,self.questionnowid,papernum,self.tihaolayout)
        display.display()
    def changetihao(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        questionall = session.query(question.id).filter(
            question.course_name == self.coursename).all()
        try:

            self.questionnowid = questionall[self.nowid - 1].id
        except:
            QtWidgets.QMessageBox.information(self, '题号', '超出题目范围')
        session.close()
        # self.lineEdit.setText(str(self.nowid))


    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '训练',
                                               "是否要退出训练？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()

    def inittihaodisplay(self):
        papernum = len(self.questionresall)
        rownum=papernum//25+1
        clonum=25
        tihao=1
        for i in range(rownum):
            for j in range(clonum):
                if tihao > papernum:
                    break
                checkboxname = "tihao" + str(tihao)
                checkbox = QtWidgets.QPushButton()
                checkbox.setFixedSize(60,25)

                checkbox.setObjectName(checkboxname)
                checkbox.setText(str(tihao))
                self.tihaolayout.addWidget(checkbox, i,j)

                checkbox.clicked.connect(partial(self.jumptihao, checkbox.text()))
                tihao += 1
    def jumptihao(self,buttext):
        self.questionnowid=int(buttext)-1
        self.xianshitimu()