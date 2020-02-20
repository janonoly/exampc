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
        self.questionnowid=0
        self.pushButton.clicked.connect(self.shangyiti)
        self.pushButton_2.clicked.connect(self.xiayiti)
        self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)
        self.pushButton_5.clicked.connect(self.tijiaodaan)


    def tijiaodaan(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        questionid=self.paperlist[self.questionnowid][0]
        questionres = session.query(question.questionType).filter(
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


        session.close()
        uers=userdaan

    def shangyiti(self):
        self.questionnowid-=1
        self.xianshitimu()

    def xiayiti(self):
        self.questionnowid+=1
        self.xianshitimu()

    def xianshitimu(self):
        #题目内容
        from controllers.utils.displayques import displayques

        questionid=self.questionnowid
        display = displayques(self,self.textBrowser, self.gridtalLayout1, questionid,self.coursename,self.questionnowid,20,self.gridtalLayout1)
        display.display()


    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.inittempuser()
            event.accept()
        else:
            event.ignore()


