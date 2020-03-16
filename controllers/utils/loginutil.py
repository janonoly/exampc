import configparser

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QPainter
from PyQt5.QtWidgets import QMessageBox, QWidget

class CommonUtil(object):
    APP_ICON = r'./resources/logo.jpg'
    def hint_dialog(widget: QWidget, icon_path: str, title: str, content: str) -> None:
        """
        display a dialog with choose button
        :param widget: the dialog rely on the father window
        :param icon_path: the dialog icon path
        :param title: the dialog title word
        :param content: the dialog content is used to hint user's
        :return: None
        """
        tip_box = QMessageBox(QMessageBox.Information, title, content)
        tip_box.setWindowIcon(QIcon(icon_path))
        submit = tip_box.addButton(widget.tr('确定'), QMessageBox.YesRole)
        tip_box.setModal(True)
        tip_box.exec_()
        if tip_box.clickedButton() == submit:
            pass
        else:
            return
    def set_button_style1_withimage(widget: QWidget, filepath):
        widget.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background :transparent}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(filepath), QIcon.Normal, QIcon.Off)
        widget.setIcon(icon)
        widget.setIconSize(QtCore.QSize(60,60))
        widget.setAutoRepeatDelay(200)

    def set_button_style_withonlyimage(widget: QWidget, filepath):
        widget.setStyleSheet("QPushButton{color:black}"
                             "QPushButton:hover{color:red}"
                             "QPushButton{background :transparent}"
                             "QPushButton{border:2px}"
                             "QPushButton{border-radius:10px}"
                             "QPushButton{padding:2px 4px}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(filepath), QIcon.Normal, QIcon.Off)
        widget.setIcon(icon)
        width=widget.rect().width()
        heigth = widget.rect().height()
        widget.setIconSize( QtCore.QSize(width, heigth))
        widget.setAutoRepeatDelay(200)
    def set_combobox_style1(widget: QWidget):
        widget.setStyleSheet("QComboBox{color:black}"
                             "QComboBox{border:4px}"
                             "QComboBox{background :#5aabe3}"
                             "QComboBox{font-family:宋体}"
                             "QComboBox{font-size:22px}"
                             "QComboBox{padding:2px 2px}")

    def set_button_style1(widget: QWidget):
        widget.setStyleSheet("QPushButton{color:white}"
                             "QPushButton:hover{color:red}"
                             "QPushButton{background :#5aabe3}"
                             "QPushButton{border:2px}"
                             "QPushButton{font-family:宋体}"
                             "QPushButton{border-radius:10px}"
                             "QPushButton{padding:2px 4px}")

    def set_horizontalline_style(widget: QWidget):
        widget.setStyleSheet("QHorizontalLine{color:black}"
                             "QHorizontalLine{background :green}"
                             )

    def set_treewiget_style1(widget: QWidget):
        widget.setStyleSheet("QTreeWidget{color:black}"
                             "QTreeWidget::item:hover{color:red}"
                             "QTreeWidget{background :transparent}"
                             "QTreeWidget{font-size:16px}"
                             "QTreeWidget::item{height:50px}"
                         )




    def set_button_style2(widget: QWidget):
        widget.setStyleSheet("QPushButton{color:white}"
                             "QPushButton:hover{color:red}"
                             "QPushButton{background :transparent}"
                             "QPushButton{border:2px}"
                             "QPushButton{border-radius:10px}"
                             "QPushButton{padding:2px 4px}")

    def set_button_style3(widget: QWidget):
        widget.setStyleSheet("QPushButton{color:black}"
                             "QPushButton:hover{color:red}"
                             "QPushButton{background :lightgreen}"
                             "QPushButton{border:2px}"
                             "QPushButton{border-radius:10px}"
                             "QPushButton{padding:2px 4px}")

    def set_button_style4(widget: QWidget):
        widget.setStyleSheet("QPushButton{color:black}"
                             "QPushButton:hover{color:white}"
                             "QPushButton{background :lightgreen}"
                             "QPushButton{border:2px}"
                             "QPushButton{border-radius:10px}"
                             "QPushButton{padding:2px 4px}")
    def set_label_style1(widget: QWidget):
            widget.setStyleSheet("QLabel{color:white}"
                                 "QLabel{border:2px}"
                                 "QLabel{border-radius:10px}"
                                 "QLabel{font-family:宋体}"
                                 "QLabel{word-wrap:true}"
                                 "QLabel{font-size:30px}"
                                 "QLabel{padding:2px 2px}")

    def set_label_style2(widget: QWidget):
        widget.setStyleSheet("QLabel{color:black}"
                             "QLabel{border:2px}"
                             "QLabel{border-radius:10px}"
                             "QLabel{word-wrap:true}"
                             "QLabel{padding:2px 2px}")
    def set_linedit_style1(widget: QWidget):
        widget.setStyleSheet("QPushButton{color:black}"
                                      "QLineEdit{background :white}"
                                      "QLineEdit{border:2px}"
                                      "QLineEdit{border-radius:10px}"
                                      "QLineEdit{padding:2px 4px}")

    def set_checkbox_style1(widget: QWidget):
        widget.setStyleSheet("QCheckBox{color:white}"
                             "QCheckBox{border:2px}"
                             "QCheckBox{border-radius:10px}"
                             "QCheckBox{padding:2px 4px}")

    def set_groupbox_style_withimage(widget: QWidget,filepath=''):
        widget.setStyleSheet("QGroupBox{color:transparent}"
                             "QGroupBox{border:none}"
                             "QGroupBox{background :transparent}"
                             "QGroupBox{border-radius:10px}"
                             "QGroupBox{padding:2px 4px}"
                             "QGroupBox{background-image: url("+filepath+")}"

                            )
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(filepath)))
        # widget.setPalette(palette)
        # widget.setStyleSheet()
        # painter = QPainter(widget)
        # painter.drawRect(widget.rect())
        # pixmap = QPixmap(filepath)  # 换成自己的图片的相对路径
        # painter.drawPixmap(widget.rect(), pixmap)

    def set_groupbox_style(widget: QWidget):
        widget.setStyleSheet("QGroupBox{color:transparent}"
                             "QGroupBox{border:none}"
                             "QGroupBox{background :transparent}"
                             "QGroupBox{border-radius:10px}"
                             "QGroupBox{padding:2px 4px}"

                             )
class ConfigParser(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.inipath = r'./config/config.ini'
        self.conf.read(self.inipath, encoding="utf-8")

    def set_user(self, username, password):
        self.conf.set('user', 'username', username)
        self.conf.set('user', 'password', password)
        self.conf.write(open(self.inipath,"r+", encoding="utf-8"))

    def get_username(self):
        return self.conf.get('user','username')

    def get_pass(self):
        return self.conf.get('user', 'password')
