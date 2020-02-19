from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from PyQt5 import QtWidgets
from model.createdb import engine
from model.question import question

class displayques(object):
    def __init__(self,chuangti,quescontentlabel,quesoptionlayout,questionid,coursename):
        self.quescontentlabel=quescontentlabel
        self.quesoptionlayout=quesoptionlayout
        self.questionid=questionid
        self.coursename = coursename
        self.chuangti=chuangti



    def initmxzdisplay(self):
        for i in range(6):
            checkboxname = "mxz" + str(i)
            checkbox = QtWidgets.QCheckBox()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)

            labelname = "mxzl" + str(i)
            label = QtWidgets.QLabel()
            label.setObjectName(labelname)
            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initxzdisplay(self):
        for i in range(6):
            checkboxname = "xz" + str(i)
            checkbox = QtWidgets.QRadioButton()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)

            labelname = "xzl" + str(i)
            label = QtWidgets.QLabel()
            label.setObjectName(labelname)
            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initpddisplay(self):
        for i in range(2):
            checkboxname = "pd" + str(i)
            checkbox = QtWidgets.QRadioButton()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)

            labelname = "pdl" + str(i)
            label = QtWidgets.QLabel()
            label.setObjectName(labelname)
            if i==0:
                label.setText('对')
            if i==1:
                label.setText('错')
            self.quesoptionlayout.addWidget(checkbox, i, 1)
            self.quesoptionlayout.addWidget(label, i, 2, 1, 200)
    def initjddisplay(self):
            checkboxname = "jd"
            checkbox = QtWidgets.QTextEdit()
            checkbox.setObjectName(checkboxname)
            checkbox.resize(20, 10)
            self.quesoptionlayout.addWidget(checkbox)

    def removeallwiget(self):
        for i in range(self.quesoptionlayout.count()):
            self.quesoptionlayout.itemAt(i).widget().deleteLater()




    def display(self):
        #先清空layout中的wiget
        self.removeallwiget()
        Session = sessionmaker(bind=engine)
        session = Session()
        questionres = session.query(question).filter(and_(question.id ==self.questionid , question.course_name == self.coursename)).first()
        #显示题目内容
        self.quescontentlabel.setText(questionres.content)

        # labelname = "labelname" + str(1)
        # label = QtWidgets.QLabel()
        # label.setText("content")
        # label.setObjectName(labelname)
        # self.quesoptionlayout.addWidget(label, 1, 2, 1, 200)


        if questionres.questionType=='xz':
             self.initxzdisplay()

        elif questionres.questionType == 'pd':
            self.initpddisplay()
        elif questionres.questionType == 'mxz':
            self.initmxzdisplay()
            #
            # if len(questionres.choice_a)>2:
            #     self.dismxz(1,questionres.choice_a)
            # if len(questionres.choice_b)>2:
            #     self.dismxz(2,questionres.choice_b)
            # if len(questionres.choice_c)>2:
            #     self.dismxz(3,questionres.choice_c)
            # if len(questionres.choice_d)>2:
            #     self.dismxz(4,questionres.choice_d)
            # if len(questionres.choice_e)>2:
            #     self.dismxz(5,questionres.choice_e)
            # if len(questionres.choice_f)>2:
            #     self.dismxz(6,questionres.choice_f)







        elif questionres.questionType == 'jd':
            self.initjddisplay()

    def dismxz(self,i,content):


        checkboxname = "mxzcheckbox" + str(i)
        checkbox = QtWidgets.QCheckBox()
        checkbox.setObjectName(checkboxname)
        checkbox.resize(20, 10)

        labelname = "mxzlabelname" + str(i)
        label = QtWidgets.QLabel()
        label.setText(content)
        label.setObjectName(labelname)
        self.quesoptionlayout.addWidget(checkbox, i, 1)
        self.quesoptionlayout.addWidget(label, i, 2, 1, 200)

    def dispd(self):


        checkboxname = "radio" + str(1)
        checkbox = QtWidgets.QRadioButton()
        checkbox.setObjectName(checkboxname)
        labelname = "radio" + str(1)
        label = QtWidgets.QLabel()
        label.setText("对")
        label.setObjectName(labelname)
        self.quesoptionlayout.addWidget(checkbox, 1, 1)
        self.quesoptionlayout.addWidget(label, 1, 2, 1, 200)




