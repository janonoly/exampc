
from PyQt5.QtGui import QIcon,  QPixmap, QPainter
from PyQt5.QtWidgets import QWidget
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import and_

from controllers.importexcel import mywindow
from model.createdb import engine
from views.login import Ui_Dialog
from controllers.utils.loginutil import CommonUtil,ConfigParser
from model.user import user

class LoginWindow( QWidget,  Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.ui1 = mywindow()
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton.clicked.connect(self.login)


    def init_ui(self):
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        CommonUtil.set_button_style2(self.pushButton_2)
        CommonUtil.set_button_style2(self.pushButton)
        CommonUtil.set_label_style1(self.label_3)
        CommonUtil.set_label_style2(self.label_2)
        CommonUtil.set_label_style2(self.label)
        CommonUtil.set_checkbox_style1(self.checkBox)
        CommonUtil.set_linedit_style1(self.lineEdit)
        CommonUtil.set_linedit_style1(self.lineEdit_2)
        self.checkBox.setChecked(True)
        conf = ConfigParser()
        self.lineEdit.setText(conf.get_username())
        self.lineEdit_2.setText(conf.get_pass())

    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap(r'./resources/login2.png')  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def login(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:

            currentuser=self.lineEdit.text().strip()
            currentpass=self.lineEdit_2.text().strip()
            users = session.query(user).filter(and_(user.name == currentuser,user.password==currentpass))
            if users.count()>=1:
                #设置config.ini
                conf = ConfigParser()
                conf.set_user(currentuser, currentpass)
                self.close()
                self.ui1.currentuser=currentuser
                self.ui1.show()
            else:
                CommonUtil.hint_dialog(self, CommonUtil.APP_ICON, '提示', '用户名或密码错误')
                return
        except Exception as e:
            print(e.args)
        finally:
            session.close()

    def register(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
                CommonUtil.hint_dialog(self, CommonUtil.APP_ICON, '提示', '请输入用户名和密码')
                return

            users = session.query(user).filter(user.name == self.lineEdit.text())
            if users.count()>=1:
                CommonUtil.hint_dialog(self, CommonUtil.APP_ICON, '提示', '用户已经存在~')
                return
            else:
                newuser=user()
                newuser.name=self.lineEdit.text().strip()
                newuser.password=self.lineEdit_2.text().strip()
                session.add(newuser)
                session.commit()
        except Exception as e:
            print(e.args)
        finally:
            session.close()



