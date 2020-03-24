import os

import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from model.question import question
from model.createdb import engine
from PyQt5.QtWidgets import QWidget, QFileDialog
from views.daochutiku import  Ui_Dialog


class Daochutikuform(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.initcomboBox()
        self.pushButton.clicked.connect(self.daochutiku)
    def initcomboBox(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        try:
            result = session.query(question.course_name).filter().distinct().all()
            self.comboBox.addItems( i.course_name for i in result)

        except:
            pass
        session.close()

    def daochutiku(self):
        try:
            w = xlwt.Workbook(encoding='utf-8')
            style = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = "微软雅黑"  # 如果是 python2 ，需要这样写 u"微软雅黑"
            style.font = font  # 为样式设置字体
            ws = w.add_sheet("题库", cell_overwrite_ok=True)
            # 将 title 作为 Excel 的列名
            title = "course_name,questionType,content,answer,zhangjie,dengji,choice_a,choice_b,choice_c,choice_d,choice_e,choice_f,choice_g,contentimg"
            title = title.split(",")
            for i in range(len(title)):
                ws.write(0, i, title[i], style)
            # 开始写入数据库查询到的数据
            Session = sessionmaker(bind=engine)
            # 每次执行数据库操作时，都需要创建一个session
            session = Session()
            rows = session.query(question).filter(question.course_name==self.comboBox.currentText()).all()
            for i in range(len(rows)):
                row = rows[i]

                ws.write(i + 1, 0, row.course_name, style)
                ws.write(i + 1, 1, row.questionType.code, style)
                ws.write(i + 1, 2, row.content, style)
                ws.write(i + 1, 3, row.answer, style)
                ws.write(i + 1, 4, row.zhangjie, style)
                ws.write(i + 1, 5, row.dengji, style)
                ws.write(i + 1, 6, row.choice_a, style)
                ws.write(i + 1, 7, row.choice_b, style)
                ws.write(i + 1, 8, row.choice_c, style)
                ws.write(i + 1, 9, row.choice_d, style)
                ws.write(i + 1, 10, row.choice_e, style)
                ws.write(i + 1, 11, row.choice_f, style)
                ws.write(i + 1, 12, row.choice_g, style)
                imgpath=os.getcwd()+'\\'+row.contentimg
                ws.write(i + 1, 13, imgpath, style)

                # for j in range(len(row)):
                #     if row[j]:
                #         item = row[j]
                #         ws.write(i + 1, j, item, style)

            # 写文件完成，开始保存xls文件
            fileName, ok2 = QFileDialog.getSaveFileName(self,
                                                        "文件保存",
                                                        "./",
                                                        "All Files (*);;Text Files (*.xls)")
            self.filepath, self.filename = os.path.split(fileName)
            path = fileName

            w.save(path)
            session.close()
            QtWidgets.QMessageBox.information(self, '导出题库', '导出成功')
        except:
            QtWidgets.QMessageBox.information(self, '导出题库', '导出失败')
