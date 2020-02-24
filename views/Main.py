# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 250, 170, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 250, 170, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.menuimpexl = QtWidgets.QAction(MainWindow)
        self.menuimpexl.setObjectName("menuimpexl")
        self.action_F = QtWidgets.QAction(MainWindow)
        self.action_F.setObjectName("action_F")
        self.action_S = QtWidgets.QAction(MainWindow)
        self.action_S.setObjectName("action_S")
        self.action_K = QtWidgets.QAction(MainWindow)
        self.action_K.setObjectName("action_K")
        self.action_D = QtWidgets.QAction(MainWindow)
        self.action_D.setObjectName("action_D")
        self.menu.addAction(self.action_F)
        self.menu.addAction(self.action_D)
        self.menu_3.addAction(self.action_K)
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "训练系统"))
        self.pushButton.setText(_translate("MainWindow", "考试"))
        self.pushButton_2.setText(_translate("MainWindow", "训练"))
        self.menu.setTitle(_translate("MainWindow", "导入题库"))
        self.menu_3.setTitle(_translate("MainWindow", "增加科目"))
        self.menuimpexl.setText(_translate("MainWindow", "导入题库(&F)"))
        self.action_F.setText(_translate("MainWindow", "导入题库(&F)"))
        self.action_S.setText(_translate("MainWindow", "选择训练科目(&S)"))
        self.action_K.setText(_translate("MainWindow", "科目设置(&K)"))
        self.action_D.setText(_translate("MainWindow", "删除题库&D"))
