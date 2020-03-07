import sys

from PyQt5.QtGui import QIcon
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from model.createdb import engine
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from views.selectcourse import  Ui_Dialog


class selectcourseform(QWidget,Ui_Dialog):
    def __init__(self,currentuser):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.state=0 #0考试1位训练
        self.currentuser=currentuser
        self.initcomboBox()
        self.initcombzhangjie()
        self.comboBox.currentTextChanged.connect(self.initcombzhangjie)
        self.pushButton.clicked.connect(self.exam)


    def initcomboBox(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import courselist
        try:
            result = session.query(courselist).all()
            # for single in result:
            #     # print('username:%s' % single.coursename)
            self.comboBox.addItems( i.coursename for i in result)
        except:
            pass
        session.close()
    def initcombzhangjie(self):
        #清空
        self.comboBox_2.clear()
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import question
        try:
            result = session.query(question.zhangjie).filter(question.course_name==
            self.comboBox.currentText()).distinct().all()
            # for single in result:
            #     # print('username:%s' % single.coursename)
            # self.comboBox_2.addItems(  '第'+str(i.zhangjie)+'章'  for i in result)
            self.comboBox_2.addItems(str(i.zhangjie) for i in result)
        except:
            pass
        session.close()
    # 定义槽函数
    @pyqtSlot()
    def exam(self):
        if self.state:
            from controllers.exam import examfrom
            self.examui = examfrom()
            # self.examui.setWindowModality(Qt.ApplicationModal)
            coursename=self.comboBox.currentText()
            hznagjie = self.comboBox_2.currentText()
            self.examui.coursename=coursename
            self.examui.curentusername = self.currentuser
            if self.radioButton_2.isChecked():
                pass
            else:
                self.examui.zhangjie = int(hznagjie)

            self.examui.show()
            # self.examui.showFullScreen()
            self.examui.showMaximized()
            self.close()
        else:
            from controllers.train1 import trainfrom
            self.trainfromui = trainfrom()
            # self.examui.setWindowModality(Qt.ApplicationModal)
            coursename = self.comboBox.currentText()
            hznagjie = self.comboBox_2.currentText()
            self.trainfromui.coursename = coursename
            if self.radioButton_2.isChecked():
                pass
            else:
                self.trainfromui.zhangjie = int(hznagjie)

            self.trainfromui.show()
            # self.examui.showFullScreen()
            self.trainfromui.showMaximized()
            self.close()

    # # 定义槽函数
    # @pyqtSlot()
    # def train(self):
    #     from controllers.train import trainfrom
    #     self.examui = trainfrom()
    #     # self.examui.setWindowModality(Qt.ApplicationModal)
    #     coursename = self.comboBox.currentText()
    #     self.examui.coursename = coursename
    #     self.examui.show()













def excel_into_model(model_name, excel_file):
    Session = sessionmaker(bind=engine)

    # 每次执行数据库操作时，都需要创建一个session
    session = Session()
    table = excel_file.sheets()[0]  # 获取第一签页
    rows = table.nrows  # 行数
    cols = table.ncols  # 列数
    colnames = table.row_values(0)  # 获取第一行一般是类别名字

    field_name = []
    # 只导入第一个sheet中的数据
    table = excel_file.sheet_by_index(0)
    nrows = table.nrows
    table_header = table.row_values(0)
    from model.question import question
    for cell in table_header:
        field_name.append(cell)
    try:
        for x in range(1, nrows):
            # 行的数据,创建对象,进行报错数据
            obj=question()
            print(len(field_name))
            for y in range(len(field_name)):
                tempfildname=field_name[y]
                cell_value=table.cell_value(x, y)
                tempstr = 'obj.%s' % field_name[y] + '=cell_value'
                exec(tempstr)
            session.add(obj)
            session.commit()
    except:
        pass
    finally:
        session.close()






