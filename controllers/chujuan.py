import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem

from model.createdb import engine
from views.chujuan import  Ui_Dialog
from controllers.utils.createpaper import createpaper
from controllers.utils.exporttoword import ExportToWord, RandExportToWord


class chujuanform(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.pushButton.clicked.connect(self.exportpaper)
        self.inittree()


    def exportpaper(self):

        try:
             papernum=int(self.lineEdit.text())
             fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "./",
                                                         "All Files (*);;Text Files (*.docx)")
             self.filepath, self.filename = os.path.split(fileName)
             self.coursename = '数学'
             for i in range(1, papernum + 1):

                 from controllers.utils.createpaper import random_createpaper
                 zhuanyedict = {'数学': ['第一章', '第二章'], '英语': ['第三章','第四章']}
                 dengjilist = ['五级', '四级']
                 zhuanyetishudict = {'数学': {'xz':1,'mxz':1,'pd':1,'tk':1,'jd':1}, '英语': {'xz':1,'mxz':1,'pd':1,'tk':0,'jd':0}}
                 timuleixingshudict = {'单选题': 20, '多选题': 20, '判断题': 20, '填空题': 20, '简答题': 20}
                 rand = random_createpaper(zhuanyedict, dengjilist, zhuanyetishudict, timuleixingshudict)
                 questionidlist=rand.create_random_paper()
                 if not questionidlist:
                     QtWidgets.QMessageBox.information(self, '出卷', '出卷失败')
                 else:
                     # paper = createpaper(self.coursename)
                     # questionidlist = paper.createpaper()
                     # questionidlist.pop()
                     try:
                         exporttoword = RandExportToWord(self.filepath, self.filename)
                         exporttoword.exportpaper(str(i), questionidlist)
                     except:
                         QtWidgets.QMessageBox.information(self, '出卷', '出卷失败')
                     # exporttoword = ExportToWord(self.filepath, self.filename, self.coursename)
                     # exporttoword.exportpaper(str(i), questionidlist)

        except:
            QtWidgets.QMessageBox.information(self, '出卷', '请输入正确数字')
    def inittree(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        self.treeWidget_2.setColumnCount(1)

        shaixuanroot = QTreeWidgetItem(self.treeWidget_2)
        shaixuanroot.setText(0, '模拟考试')
        shaixuanroot.setCheckState(0, not Qt.CheckState)

        child2 = QTreeWidgetItem(shaixuanroot)

        child2.setText(0, 'child2')
        child2.setCheckState(0, not Qt.CheckState)
        session.close()

        # self.treeWidget_2.expandAll()

