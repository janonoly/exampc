import os

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from PyQt5 import QtWidgets, QtGui
from model.createdb import engine
from model.question import question,tempuserans
from controllers.loginview import CommonUtil
class displayques(object):
    def __init__(self,chuangti,quescontentlabel,quesoptionlayout,questionid,coursename,tihao,papernum,tihaolayout,tuxiangview):
        # super().__init__()
        # self.setupUi(self)
        self.quescontentlabel=quescontentlabel
        self.quesoptionlayout=quesoptionlayout


        self.questionid=questionid
        self.coursename = coursename
        self.chuangti=chuangti
        self.tihao=tihao
        self.papernum=papernum
        self.tihaolayout=tihaolayout
        self.tuxiangview=tuxiangview
        # self.inittihaodisplay()
        self.userans=self.getuseran()
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(14)




    def getuseran(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        tempuseran = session.query(tempuserans).filter(
            tempuserans.question_id==self.questionid ).first()
        userans=''
        if tempuseran :
            userans = tempuseran.userans
        return userans
    def initmxzdisplay(self):

        tempkey = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for i in range(7):
            checkboxname = "daan" + str(i)
            checkbox = QtWidgets.QCheckBox()
            checkbox.setObjectName(checkboxname)
            checkbox.setFont(self.font)
            checkbox.resize(20, 10)
            tempkeyl=tempkey[i]
            if tempkeyl in self.userans:
                checkbox.setChecked(True)
            labelname = "mxzl" + str(i)
            label = QtWidgets.QLabel()
            label.setObjectName(labelname)
            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initxzdisplay(self):
        tempkey = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for i in range(7):
            checkboxname = "daan" + str(i)
            checkbox = QtWidgets.QRadioButton()
            checkbox.setObjectName(checkboxname)
            checkbox.setFont(self.font)
            checkbox.resize(20, 10)

            from controllers.utils.loginutil import CommonUtil
            CommonUtil.set_radio_stylewithimage(checkbox)

            tempkeyl=tempkey[i]
            if tempkeyl in self.userans:
                checkbox.setChecked(True)
            labelname = "xzl" + str(i)
            label = QtWidgets.QLabel()

            label.setFont(self.font)
            label.setObjectName(labelname)
            # self.quesoptionlayout.addWidget(checkbox)
            # self.quesoptionlayout.addWidget(label)

            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initpddisplay(self):
        for i in range(2):
            checkboxname = "daan" + str(i)
            checkbox = QtWidgets.QRadioButton()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)
            if i==0:
                if self.userans=='True':
                    checkbox.setChecked(True)
            if i==1:
                if self.userans=='False':
                    checkbox.setChecked(True)

            labelname = "pdl" + str(i)
            label = QtWidgets.QLabel()

            label.setFont(self.font)
            label.setObjectName(labelname)
            if i==0:
                label.setText('对')
            if i==1:
                label.setText('错')
            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initjddisplay(self):
            checkboxname = "daan"
            checkbox = QtWidgets.QTextEdit()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)
            checkbox.setFont(self.font)
            checkbox.setText(self.userans)
            self.quesoptionlayout.addWidget(checkbox)
    def inittkdisplay(self):
            checkboxname = "daan"
            checkbox = QtWidgets.QTextEdit()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)
            checkbox.setFont(self.font)
            checkbox.setText(self.userans)
            self.quesoptionlayout.addWidget(checkbox)

    def removeallwiget(self):
        for i in range(self.quesoptionlayout.count()):
            self.quesoptionlayout.itemAt(i).widget().deleteLater()
    def inittihaodisplay(self):
        clonum=self.papernum//3
        rownum=4
        tihao=0
        for i in range(rownum):

            for j in range(clonum):
                checkboxname = "tihao" + str(tihao)
                checkbox = QtWidgets.QPushButton()
                checkbox.setObjectName(checkboxname)
                checkbox.setFont(self.font)
                checkbox.setText(str(tihao))
                self.tihaolayout.addWidget(checkbox, i,j)
                checkbox.clicked.connect(self.jumptihao)

                tihao += 1
                if tihao > self.papernum :
                    break
        # for i in range(self.tihaolayout.count()):
        #     self.tihaolayout.itemAt(i).widget().clicked.connect(self.jumptihao)


    def jumptihao(self):
        print("1")
    def display(self):
        #先清空layout中的wiget
        self.removeallwiget()
        Session = sessionmaker(bind=engine)
        session = Session()
        questionres = session.query(question).filter(and_(question.id ==self.questionid , question.course_name == self.coursename)).first()
        #显示题目内容
        dictquestiontype={ 'xz':'选择题','mxz':'多选题', 'jd':'简答题', 'tk':'填空题', 'pd':'判断题' }
        timuleixing =''
        try:
            timuleixing = dictquestiontype[questionres.questionType]
        except:
            pass
        tempstr='('+timuleixing+')'+str(self.tihao+1)+': '+questionres.content
        self.quescontentlabel.setText(tempstr)


        if questionres.contentimg:
            self.tuxiangview.setHidden(False)
            imgfilepath=os.getcwd()+'\\'+questionres.contentimg
            CommonUtil.set_button_style_withonlyimage(self.tuxiangview,imgfilepath)
        else:
            self.tuxiangview.setHidden(True)

        # labelname = "labelname" + str(1)
        # label = QtWidgets.QLabel()
        # label.setText("content")
        # label.setObjectName(labelname)
        # self.quesoptionlayout.addWidget(label, 1, 2, 1, 200)


        if questionres.questionType=='xz':
             self.initxzdisplay()
             qlist = self.chuangti.findChildren(QtWidgets.QRadioButton)
             self.displayoption(questionres,qlist)
        elif questionres.questionType == 'pd':
            self.initpddisplay()
        elif questionres.questionType == 'mxz':
            self.initmxzdisplay()
            qlist = self.chuangti.findChildren(QtWidgets.QCheckBox)
            self.displayoption(questionres, qlist)
        elif questionres.questionType == 'jd':
            self.initjddisplay()
        elif questionres.questionType == 'tk':
            self.inittkdisplay()



    def displayoption(self,questionres,qlist):

        flag = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        flag1 = 0
        for x in qlist:
            # x.setText(questionres.choice_a)

            tempstr = 'x.setText(questionres.choice_%s)' % flag[flag1]
            temstr1='if len(questionres.choice_%s) ' % flag[flag1] +' > 2 : '+tempstr+' '
            temstr2 = 'if len(questionres.choice_%s) ' % flag[flag1] + ' <= 2 :   x.setHidden(True) '
            exec(temstr1)
            exec(temstr2)
            flag1 += 1




