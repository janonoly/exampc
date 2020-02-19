import sys

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
        self.action_F.triggered.connect(self.impquefrmexl)
        self.action_K.triggered.connect(self.addcourse)
        self.pushButton.clicked.connect(self.exam)
        self.pushButton_2.clicked.connect(self.train)
        self.initcomboBox()
    def addcourse(self):
        from controllers.addcourse import myform1
        self.ui=myform1()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()

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
        from controllers.exam import examfrom
        self.examui = examfrom()
        self.examui.setWindowModality(Qt.ApplicationModal)
        coursename=self.comboBox.currentText()
        self.examui.coursename=coursename
        self.examui.show()







    # 定义槽函数
    @pyqtSlot()
    def train(self):
        QMessageBox.information(self, '导入', '导入成功')











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






