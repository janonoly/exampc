import sys

from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter, QIcon
from sqlalchemy.orm import sessionmaker
from model.createdb import engine
from PyQt5 import QtWidgets
from xlrd import open_workbook
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
from views.Main import  Ui_MainWindow




class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.setstyle()
        self.action_F.triggered.connect(self.impquefrmexl)
        self.action_K.triggered.connect(self.addcourse)
        self.action_D.triggered.connect(self.deletequestion)
        self.pushButton.clicked.connect(self.exam)
        self.pushButton_2.clicked.connect(self.train)
        self.inittempuser()
    def setstyle(self):
        # # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 无边框，置顶
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景色
        self.setWindowIcon(QIcon('./resources/logo.jpg'))
        # self.pushButton.setIcon(QIcon("./resources/logo.jpg"))
        # self.pushButton.setIcon(QIcon("./resources/logo.jpg"))
        self.pushButton.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:lightgreen}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.pushButton_2.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:lightgreen}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.label.setText("单机考试系统V1.0")

    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("./resources/background.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def deletequestion(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        from model.question import question
        # result = session.query(tempuserans).all()
        # session.delete(result)
        reply = QtWidgets.QMessageBox.question(self,
                                               '删除题库',
                                               "是否要删除题库？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            session.query(question).filter().delete()
            session.commit()
        else:
            pass

        session.close()
    def inittempuser(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        from model.question import tempuserans
        # result = session.query(tempuserans).all()
        # session.delete(result)
        session.query(tempuserans).filter().delete()
        session.commit()
        session.close()
    def addcourse(self):
        from controllers.addcourse import myform1
        self.ui=myform1()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()
    #定义槽函数
    @pyqtSlot()
    def impquefrmexl(self):
       #打开文件管理器

       # path=self.load_last_path()
       file = QDialog()
       fname, ftype = QFileDialog.getOpenFileName(file, 'open')
       # fname='C:/Users/MSI-PC/Desktop/exams_question.xls'
       if 'xls' in fname:
           # 处理逻 辑
           try:
               files = open_workbook(filename=fname)
               excel_into_model(model_name='question', excel_file=files)
               QMessageBox.information(self, '导入', '导入成功')
           except:
               QMessageBox.information(self, '导入', '导入失败')

    # 定义槽函数
    @pyqtSlot()
    def exam(self):
        from controllers.selectcourse import selectcourseform
        self.examui = selectcourseform()
        self.examui.state=1
        self.examui.setWindowModality(Qt.ApplicationModal)
        self.examui.show()

    # 定义槽函数
    @pyqtSlot()
    def train(self):
        from controllers.selectcourse import selectcourseform
        self.examui = selectcourseform()
        self.examui.state = 0
        self.examui.setWindowModality(Qt.ApplicationModal)
        self.examui.show()













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






