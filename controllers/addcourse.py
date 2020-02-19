from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from sqlalchemy.orm import sessionmaker
from model.createdb import engine

from views.addcourseview import Ui_Dialog

class myform1(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.addcourse)
        self.pushButton_2.clicked.connect(self.updateshezhi)
        self.pushButton_3.clicked.connect(self.delcource)


        self.comboBox.currentTextChanged.connect(self.initshezhi)
        self.initcomboBox()


    def initcomboBox(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import courselist
        try:
            result = session.query(courselist).all()
            # for single in result:
            #     # print('username:%s' % single.coursename)
            self.comboBox.clear()
            self.comboBox.addItems( i.coursename for i in result)
        except:
            pass

        finally:
            session.close()
    def delcource(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import courselist,PaperList
        coursename=self.comboBox.currentText()
        try:
            result = session.query(PaperList).filter(PaperList.course_name == coursename).first()
            session.delete(result)
            session.commit()
        except:
            pass
        try:
            result1 = session.query(courselist).filter(courselist.coursename == coursename).first()
            session.delete(result1)
            session.commit()
            QMessageBox.information(self, '删除', '删除成功')
        except:
            QMessageBox.information(self, '删除', '删除失败')
        finally:
            session.close()
        self.initcomboBox()

    def initshezhi(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import PaperList

        cousrcename=self.comboBox.currentText()
        try:
            result = session.query(PaperList).filter(PaperList.course_name == cousrcename).all()
            for paperlistre in result:
                self.lineEdit_2.setText(str(paperlistre.single_choice_num))
                self.lineEdit_3.setText(str(paperlistre.single_choice_score))
                self.lineEdit_8.setText(str(paperlistre.judgment))
                self.lineEdit_7.setText(str(paperlistre.judgment_score))
                self.lineEdit_5.setText(str(paperlistre.multiple_choice_num))
                self.lineEdit_4.setText(str(paperlistre.multiple_choice_score))
                self.lineEdit_6.setText(str(paperlistre.jd_choice_num))
                self.lineEdit_9.setText(str(paperlistre.jd_choice_score))
                self.lineEdit_10.setText(str(paperlistre.kaoshishijian))

        except:
            pass
        finally:
            session.close()



    @pyqtSlot()
    def updateshezhi(self):
        coursename = self.comboBox.currentText()
        from model.createdb import engine
        from model.question import PaperList
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()





        try:
            paperlist = session.query(PaperList).filter(PaperList.course_name == coursename).first()
            paperlist.single_choice_num = int(self.lineEdit_2.text())
            paperlist.single_choice_score = int(self.lineEdit_3.text())
            paperlist.judgment = int(self.lineEdit_8.text())
            paperlist.judgment_score = int(self.lineEdit_7.text())
            paperlist.multiple_choice_num = int(self.lineEdit_5.text())
            paperlist.multiple_choice_score = int(self.lineEdit_4.text())
            paperlist.jd_choice_num = int(self.lineEdit_6.text())
            paperlist.jd_choice_score = int(self.lineEdit_9.text())
            paperlist.kaoshishijian = int(self.lineEdit_10.text())

            session.commit()

            QMessageBox.information(self, '设置', '设置成功')
        except:
            QMessageBox.information(self, '设置', '设置失败')
        finally:
            session.close()


    @pyqtSlot()
    def addcourse(self):
        coursename=self.lineEdit.text()
        from  model.createdb import engine
        from model.question import courselist,PaperList
        Session = sessionmaker(bind=engine)

        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        obj=courselist()
        obj.coursename=coursename
        obj1 = PaperList()
        obj1.course_name = coursename

        try:
            session.add(obj1)
            session.add(obj)
            session.commit()
            QMessageBox.information(self, '导入', '导入成功')
        except:
            QMessageBox.information(self, '导入', '导入失败')
        finally:
            session.close()
        self.initcomboBox()



