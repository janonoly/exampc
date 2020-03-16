
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from model.question import question
from model.createdb import engine
from PyQt5.QtWidgets import QWidget
from views.shanchuzhuanye import  Ui_Dialog


class Shanchuzhuanyeform(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.initcomboBox()
        self.pushButton.clicked.connect(self.shanchuzhuanye)
    def initcomboBox(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        try:
            self.comboBox.clear()
            result = session.query(question.course_name).filter().distinct().all()
            self.comboBox.addItems( i.course_name for i in result)

        except:
            pass
        session.close()

    def shanchuzhuanye(self):
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
            try:
                res=session.query(question).filter(question.course_name == self.comboBox.currentText())
                # session.query(question).filter(question.course_name==self.comboBox.currentText()).delete()
                isimage=res.all()
                res.delete()
                session.commit()
                import os
                curentpath = os.getcwd()
                for i in isimage:
                    filea = os.path.isfile(curentpath + '\\' + i.choice_a)
                    fileb = os.path.isfile(curentpath+'\\'+i.choice_b)
                    filec = os.path.isfile(curentpath+'\\'+i.choice_c)
                    filed = os.path.isfile(curentpath+'\\'+i.choice_d)
                    filee = os.path.isfile(curentpath+'\\'+i.choice_e)
                    filef = os.path.isfile(curentpath+'\\'+i.choice_f)
                    files={i.choice_a:filea,i.choice_b:fileb,i.choice_c:filec,i.choice_d:filed,i.choice_e:filee,i.choice_f:filef}
                    for (k,v) in files.items():
                        if v:
                            filepath=k
                            finalpath=curentpath+'\\'+filepath
                            os.remove(finalpath)
                self.initcomboBox()
            except:
                QtWidgets.QMessageBox.information(self, '删除', self.comboBox.currentText()+'删除失败')
        else:
            pass

        session.close()
