import sys

from PyQt5.QtGui import QIcon, QPainter, QPixmap
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from model.createdb import engine
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget
from views.selectcourse import  Ui_Dialog


class selectcourseform(QWidget,Ui_Dialog):
    def __init__(self,currentuser):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))

        self.currentuser=currentuser
        self.init_style()
        self.initcombobox_leibie()

        self.comboBox_3.currentTextChanged.connect(self.initcombobox_zhuanye)
        self.comboBox.currentTextChanged.connect(self.initcombobox_zhangjie)
        self.comboBox_2.currentTextChanged.connect(self.initcombobox_dengji)
        self.pushButton_8.clicked.connect(self.train)
        self.pushButton_9.clicked.connect(self.close)

        # self.pushButton.clicked.connect(self.exam)

    def init_style(self):
        self.pushButton_8.setHidden(True)
        CommonUtil.set_combobox_style1(self.comboBox)
        CommonUtil.set_combobox_style1(self.comboBox_3)
        CommonUtil.set_combobox_style1(self.comboBox_2)
        CommonUtil.set_combobox_style1(self.comboBox_4)
        CommonUtil.set_groupbox_style(self.groupBox)
        CommonUtil.set_groupbox_style(self.groupBox_2)
        CommonUtil.set_button_style1(self.pushButton_8)
        CommonUtil.set_button_style1(self.pushButton_9)
    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("./resources/background.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)
    def initcombobox_leibie(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import courselist
        try:
            result = session.query(courselist.leibiename).distinct().all()

            self.comboBox_3.addItems( i.leibiename for i in result)
        except:
            pass
        session.close()

    def initcombobox_dengji(self):
        self.comboBox_4.clear()
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import question
        try:

            result = session.query(question.dengji).filter(question.course_name ==
                                                             self.comboBox.currentText()).distinct().all()
            self.comboBox_4.addItem('')
            self.comboBox_4.addItems(str(i.dengji) for i in result)
        except:
            pass
        finally:
            session.close()
    def initcombobox_zhangjie(self):
        self.pushButton_8.setHidden(False)
        self.comboBox_2.clear()
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import question
        try:

            result = session.query(question.zhangjie).filter(question.course_name ==
                                                                 self.comboBox.currentText()).distinct().all()
            self.comboBox_2.addItem('')
            self.comboBox_2.addItems(str(i.zhangjie) for i in result)
        except:
            pass
        finally:
            session.close()
    def initcombobox_zhuanye(self):
        #清空
        self.comboBox.clear()
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import courselist
        try:

            result = session.query(courselist.coursename).filter(courselist.leibiename==
            self.comboBox_3.currentText()).distinct().all()
            self.comboBox.addItems(str(i.coursename) for i in result)
        except:
            pass
        finally:
            session.close()

    # 定义槽函数
    @pyqtSlot()
    def train(self):

        from controllers.train1 import trainfrom
        zhuanye=self.comboBox.currentText()
        zhangjie = self.comboBox_2.currentText().strip()
        dengji = self.comboBox_4.currentText().strip()
        # if zhangjie:
        #     pass
        # else:
        #     zhangjie=None
        # if dengji:
        #     pass
        # else:
        #     dengji = None
        self.trainfromui = trainfrom(self.currentuser,zhuanye,zhangjie,dengji)
        self.trainfromui.setWindowTitle(zhuanye)
        self.trainfromui.show()

        self.trainfromui.showMaximized()
        self.close()












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






