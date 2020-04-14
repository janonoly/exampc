import os
import re
import sys

import xlsxwriter as xlsxwriter
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QPainter, QIcon
from sqlalchemy.orm import sessionmaker

from controllers.utils.copyimgtodir import CopyImgToDir
from controllers.utils.modeutil import ModelUtil
from model.createdb import engine
from PyQt5 import QtWidgets
from xlrd import open_workbook

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
from views.Main import  Ui_MainWindow
from controllers.utils.loginutil import CommonUtil
import  xlsxwriter


class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.currentuser=None
        self.setupUi(self)
        self.setstyle()
        self.action_F.triggered.connect(self.impquefrmexl)
        self.action_K.triggered.connect(self.addcourse)
        self.action_D.triggered.connect(self.deletequestion)
        self.action_L.triggered.connect(self.history)
        self.action_T.triggered.connect(self.close)
        self.action_E.triggered.connect(self.daochutiku)
        self.action_word_O.triggered.connect(self.exportpaper)
        self.actionhelp_H.triggered.connect(self.bangzhu)
        self.action_G.triggered.connect(self.guanyu)
        # self.action_J.triggered.connect(self.jianyichujuan)
        self.pushButton.clicked.connect(self.exam)
        self.pushButton_2.clicked.connect(self.traintl)
        self.pushButton_8.clicked.connect(self.trainyzyh)
        self.pushButton_7.clicked.connect(self.trainfgzd)
        self.pushButton_9.clicked.connect(self.trainzsjh)
        modelutil=ModelUtil()
        modelutil.inittempuser()

    def guanyu(self):
        QtWidgets.QMessageBox.information(self, '关于', '版本：V1.0.0  ')

    def bangzhu(self):
        from win32com import client as wc
        try:
            word=None
            try:

                word = wc.Dispatch('Word.Application')  # 打开word应用程序
            except:
                pass
            try:
                word = wc.Dispatch("Kwps.Application")
            except:
                pass
            word.Visible = True
            path =os.getcwd()+'\\'+ r'resources\帮助.docx'
            doc = word.Documents.Open(FileName=path)
        except:
            QtWidgets.QMessageBox.information(self, '帮助', '打开失败，无word应用')

    def setstyle(self):

        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        CommonUtil.set_button_style1( self.pushButton )
        CommonUtil.set_button_style1(self.pushButton_2 )
        CommonUtil.set_button_style1(self.pushButton_7 )

        CommonUtil.set_button_style1(self.pushButton_8 )
        CommonUtil.set_button_style1(self.pushButton_9)
        CommonUtil.set_groupbox_style(self.groupBox)
        CommonUtil.set_groupbox_style_withimage(self.groupBox_2,'')
        CommonUtil.set_horizontalline_style(self.line)
        self.label.setText("理论知识考核系统")


    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("./resources/background.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def deletequestion(self):
        from controllers.shanchuzhuanye import Shanchuzhuanyeform
        self.ui = Shanchuzhuanyeform()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()

    def addcourse(self):
        from controllers.addcourse import myform1
        self.ui=myform1()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()
    def daochutiku(self):
        from controllers.daochutiku import Daochutikuform
        self.ui = Daochutikuform()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()
    def exportpaper(self):

        from controllers.chujuan import chujuanform
        self.ui = chujuanform()
        self.ui.setWindowModality(Qt.ApplicationModal)
        self.ui.show()

    def jianyichujuan(self):
        from controllers.exportpaper import exportpaperform
        self.ui=exportpaperform()
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
        self.examui = selectcourseform(self.currentuser)
        self.examui.setWindowModality(Qt.ApplicationModal)
        self.examui.show()


    def history(self):
        from controllers.history import Historyfrom
        self.examui = Historyfrom(self.currentuser)
        self.examui.showMaximized()
        self.examui.setWindowModality(Qt.ApplicationModal)
        self.examui.setWindowTitle('历史成绩')
        self.examui.show()

    # 定义槽函数
    @pyqtSlot()
    def traintl(self):
        from controllers.train1 import trainfrom
        self.trainfromui = trainfrom(self.currentuser, '条令条例')
        self.trainfromui.setWindowTitle('条令条例')
        self.trainfromui.show()
        self.trainfromui.showMaximized()

        # 定义槽函数

    @pyqtSlot()
    def trainyzyh(self):
        from controllers.train1 import trainfrom
        self.trainfromui = trainfrom(self.currentuser, '应知应会')
        self.trainfromui.setWindowTitle('应知应会')
        self.trainfromui.show()

        self.trainfromui.showMaximized()

  # 定义槽函数
    @pyqtSlot()
    def trainfgzd(self):
        from controllers.train1 import trainfrom
        self.trainfromui = trainfrom(self.currentuser, '法规制度')
        self.trainfromui.setWindowTitle('法规制度')
        self.trainfromui.show()

        self.trainfromui.showMaximized()

  # 定义槽函数
    @pyqtSlot()
    def trainzsjh(self):
        from controllers.train1 import trainfrom
        self.trainfromui = trainfrom(self.currentuser, '战伤救护')
        self.trainfromui.setWindowTitle('战伤救护')
        self.trainfromui.show()

        self.trainfromui.showMaximized()













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
                cell_value=str(table.cell_value(x, y))
                # cell = table.inse(x, y)
                #如果cell_value为文件则将其存入resources/tikutupian
                # 匹配content中的图片

                regex = r'([a-zA-D]:.*\.\S*)\''
                mst = re.search(regex, cell_value)
                res=cell_value
                if mst:
                    res = mst.group(1)
                file = os.path.isfile(res)
                if file:
                    filepath, filename=os.path.split(res)
                    des_dir=r'resources\tikutupian'
                    copy = CopyImgToDir(res,des_dir)
                    copy.copy_img_to_dir()
                    cell_value=cell_value.replace(res,des_dir+'\\'+filename)
                tempstr = 'obj.%s' % field_name[y] + '=cell_value'
                exec(tempstr)
            session.add(obj)
            session.commit()
    except:
        pass
    finally:
        session.close()






