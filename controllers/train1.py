from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from controllers.utils.modeutil import ModelUtil
from model.createdb import engine
from model.question import question, tempuserans, courselist
from views.train1 import Ui_Dialog
from model.user import Collects, user, Errors


class trainfrom(QWidget,Ui_Dialog):
    def __init__(self,current_username,coursename,zhangjie='',dengji=''):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        CommonUtil.set_treewiget_style1(self.treeWidget)
        self.coursename=coursename
        self.zhangjie = zhangjie
        self.dengji = dengji
        self.current_username=current_username
        self.xunlianmoshi=0
        self.questionnowid=0
        self.pushButton.clicked.connect(self.shangyiti)
        self.pushButton_2.clicked.connect(self.xiayiti)
        # self.Layout = QtWidgets.QVBoxLayout(self.groupBox_2)
        # self.horizontalLayout.setObjectName("horizontalLayout")

        self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)
        # self.gridtalLayout1 = QtWidgets.QGridLayout(self.groupBox_2)
        self.pushButton_5.clicked.connect(self.tijiaodaan)
        self.lineEdit.installEventFilter(self)
        self.pushButton_3.clicked.connect(self.inittimu)
        self.pushButton_7.clicked.connect(self.jiaojuan)
        self.treeWidget.itemClicked.connect(self.handleChanged)
        # self.treeWidget.itemDoubleClicked.connect(self.initcheckbox)
        self.pushButton_6.clicked.connect(self.collecttimu)
        self.initbutton()
        self.inittree()
    #收藏题目功能
    def jiaojuan(self):
        from controllers.jiaojuan import juaojuan
        self.juaojuan = juaojuan(self.paperlist, self.coursename,self.current_username,self.xunlianmoshi)
        self.juaojuan.show()
    def collecttimu(self):
        modelutil = ModelUtil()
        # userinstace=modelutil.getuserinstance(self.current_username)

        questionid = self.questionresall[self.questionnowid][0]
        collect=Collects()
        collect.collectid=questionid
        # collect.userid=userinstace.id
        collect.userid = self.current_username
        save_res=modelutil.save_collect(collect)
        self.init_collectbutton1(save_res)
        modelutil.session_close()

    def init_collectbutton1(self,save_res):
        if not save_res:
            # QMessageBox.information(self,'提示','此题已收藏')
            self.pushButton_6.setText('收藏')

        else:
            # QMessageBox.information(self, '提示', '此题已收藏')
            self.pushButton_6.setText('已收藏')
    def init_collectbutton(self):

        modelutil = ModelUtil()
        userinstace = modelutil.getuserinstance(self.current_username)

        questionid = self.questionresall[self.questionnowid][0]
        collect = Collects()
        collect.collectid = questionid
        collect.userid = userinstace.id
        save_res = modelutil.get_collect(collect)

        modelutil.session_close()
        if not save_res:
            # QMessageBox.information(self,'提示','此题已收藏')
            self.pushButton_6.setText('收藏')

        else:
            # QMessageBox.information(self, '提示', '此题已收藏')
            self.pushButton_6.setText('已收藏')

    def handleChanged(self, item, column):

        text =item.text(0)
        try:
            text=item.parent().text(0)
            for i in range(item.parent().childCount()):
                if item.parent().child(i) != item:
                    item.parent().child(i).setCheckState(0, not Qt.CheckState)
                # item.setCheckState(0, Qt.Checked)

        except:
            pass

        try:
            if text == '选择章节':
                self.xunlianmoshi = 4
                self.questionnowid = 0
                self.zhangjiexl(item, column)
                self.inittimu()
            elif text == '选择科目':
                self.xuanzhekemu(item, column)

            elif text == '模拟考试':
                self.inittempuser()
                self.xunlianmoshi = 1
                self.questionnowid = 0
                self.inittimu()

            elif text == '错题训练':
                self.questionnowid = 0
                self.xunlianmoshi = 2
                self.inittimu()

            elif text == '收藏的题':
                self.questionnowid = 0
                self.xunlianmoshi = 3
                self.inittimu()
            elif text == '正式考试':
                # try:
                self.xunlianmoshi = 5
                self.close()
                self.exam()
            elif text == '训练模式':
                self.xunlianmoshi = 6
                self.questionnowid = 0
                self.inittimu()
                # except:
                #     QMessageBox.information(self, '提示', '当前题目为空')


        except:
            pass


    def exam(self):
            from controllers.exam import examfrom
            self.examui = examfrom()
            # self.examui.setWindowModality(Qt.ApplicationModal)
            coursename=self.coursename
            hznagjie = self.zhangjie
            self.examui.coursename=coursename
            self.examui.xunlianmoshi = self.xunlianmoshi
            self.examui.curentusername = self.current_username
            if hznagjie:
                self.examui.zhangjie = hznagjie
            else:
                pass

            self.examui.show()
            # self.examui.showFullScreen()
            self.examui.showMaximized()
            self.close()




    def xuanzhekemu(self, item, column):
        # if item.checkState(column) == Qt.Checked:
        # 设置头部标题
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        selected_coursename = item.text(0)
        self.coursename = selected_coursename
        try:

            zhangjieresult = session.query(question.zhangjie).filter(
                question.course_name == selected_coursename).distinct().all()
            num = self.treeWidget.topLevelItem(1).childCount()
            for i in range(num):
                self.treeWidget.topLevelItem(1).removeChild(self.treeWidget.topLevelItem(1).child(0))
            for i in zhangjieresult:
                child1 = QTreeWidgetItem(self.treeWidget.topLevelItem(1))
                child1.setText(0, '第' + str(i.zhangjie) + '章')
                child1.setCheckState(0, not Qt.CheckState)
        except:
            pass
        finally:
            session.close()

    def zhangjiexl(self,item,column):

        selected_zhangjie = item.text(0)
        self.zhangjie = int(selected_zhangjie[1])
        if item.checkState(column) != Qt.Checked:
            self.zhangjie = 0
            self.xunlianmoshi=0
        self.questionnowid = 0

    def inittree(self):
        #设置头部标题

        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        self.treeWidget.setColumnCount(1)

        # zhangjieroot = QTreeWidgetItem(self.treeWidget)
        # zhangjieroot.setText(0,'选择章节')
        # zhangjieroot.setIcon(0,QIcon('./resources/saixuan1.png'))
        zhangjieroot = QTreeWidgetItem(self.treeWidget)
        zhangjieroot.setText(0,'训练模式')
        zhangjieroot.setIcon(0,QIcon('./resources/saixuan1.png'))
        #
        # try:
        #     coursenamedefault=self.coursename
        #     zhangjieresult = session.query(question.zhangjie).filter(question.course_name == coursenamedefault).distinct().all()
        #     for i in zhangjieresult:
        #         child1 = QTreeWidgetItem(zhangjieroot)
        #         child1.setText(0, '第'+str(i.zhangjie)+'章')
        #         child1.setCheckState(0, not Qt.CheckState)
        # except:
        #     pass

        shaixuanroot = QTreeWidgetItem(self.treeWidget)
        shaixuanroot.setText(0, '模拟考试')
        shaixuanroot.setIcon(0, QIcon('./resources/monikaoshi.png'))
        #
        shaixuanroot = QTreeWidgetItem(self.treeWidget)
        shaixuanroot.setText(0, '正式考试')
        shaixuanroot.setIcon(0, QIcon('./resources/saixuan1.png'))

        cuotiroot = QTreeWidgetItem(self.treeWidget)
        cuotiroot.setText(0, '错题训练')
        cuotiroot.setIcon(0, QIcon('./resources/error1.png'))

        shouchangroot = QTreeWidgetItem(self.treeWidget)
        shouchangroot.setText(0, '收藏的题')
        shouchangroot.setIcon(0, QIcon('./resources/collect1.png'))

        session.close()

        self.treeWidget.expandAll()

    def eventFilter(self, widget, event):
        if widget == self.lineEdit:
            if event.type() == QEvent.FocusOut:
                try:
                    tiaozhuan=int(self.lineEdit.text())-1
                    if tiaozhuan >= len(self.questionresall) - 1:
                        QMessageBox.information(self, '提示', '跳转题号超出范围')
                        pass
                    else:
                        self.questionnowid=tiaozhuan
                except:
                    pass
            # elif event.type() == QEvent.FocusIn:
            #     pass# 当焦点再次落到edit输入框时，发送clicked信号出去
            # else:
            #     pass
        return False
    def initbutton(self):
        CommonUtil.set_button_style3(self.pushButton)
        CommonUtil.set_button_style3(self.pushButton_2)
        CommonUtil.set_button_style3(self.pushButton_3)
        CommonUtil.set_button_style3(self.pushButton_6)
        CommonUtil.set_button_style3(self.pushButton_5)
        CommonUtil.set_button_style3(self.pushButton_7)
        self.pushButton_2.setHidden(True)
        self.pushButton_5.setHidden(True)
        self.pushButton_6.setHidden(True)
        self.pushButton_7.setHidden(True)
        self.pushButton.setHidden(True)
        self.lineEdit.setHidden(True)
        self.label_3.setHidden(True)
        self.pushButton_4.setHidden(True)

    def inittimu(self):
        if self.coursename=='':
            QMessageBox.information(self, '提示', '请选择科目')
            return
        self.pushButton_3.setHidden(True)
        self.pushButton_7.setHidden(True)
        self.pushButton_2.setHidden(False)
        self.pushButton_5.setHidden(False)
        self.pushButton_6.setHidden(False)
        self.pushButton.setHidden(True)
        self.label_2.setHidden(False)
        self.lineEdit.setHidden(False)
        self.label_3.setHidden(False)
        Session = sessionmaker(bind=engine)
        session = Session()


        if self.xunlianmoshi==1: # 模拟训练

            self.pushButton_7.setHidden(False)
            self.label_2.setHidden(True)
            from controllers.utils.createpaper import createpaper
            paper = createpaper(self.coursename, None)
            try:
                self.paperlist = paper.createpaper()
                self.paperlist.pop()
                self.questionresall =self.paperlist
            except:
                pass
            pass
        elif self.xunlianmoshi==2: # 错题训练


            # self.questionresall = session.query(Errors.id).join(question.course_name,question.id==Errors.id).filter(and_(Errors.userid == self.current_username,question.course_name==self.coursename)).all()
            self.questionresall = session.query(Errors.errorid).join(question,question.id==Errors.errorid).filter(and_(Errors.userid==self.current_username,question.course_name==self.coursename)).all()

        elif self.xunlianmoshi == 3:  # 收藏训练

            # self.questionresall = session.query(Errors.id).join(question.course_name,question.id==Errors.id).filter(and_(Errors.userid == self.current_username,question.course_name==self.coursename)).all()
            self.questionresall = session.query(Collects.collectid).join(question, question.id == Collects.collectid).filter(
                and_(Collects.userid == self.current_username, question.course_name == self.coursename)).all()

        elif self.xunlianmoshi == 4:  # 章节训练

            self.questionresall = session.query(question.id).filter(
                and_(question.zhangjie == self.zhangjie, question.course_name == self.coursename)).all()

        else: # 不按章节训练
            if self.zhangjie and self.dengji:
                self.questionresall = session.query(question.id).filter(
                and_(question.course_name == self.coursename,question.zhangjie==self.zhangjie,question.dengji==self.dengji)).all()
            elif self.zhangjie and not self.dengji:
                self.questionresall = session.query(question.id).filter(
                    and_(question.course_name == self.coursename, question.zhangjie == self.zhangjie)).all()
            elif not self.zhangjie and  self.dengji:
                self.questionresall = session.query(question.id).filter(
                    and_(question.course_name == self.coursename, question.dengji == self.dengji)).all()
            else:
                self.questionresall = session.query(question.id).filter(
                     question.course_name == self.coursename ).all()
        if len(self.questionresall)==0:
            QMessageBox.information(self, '提示', '当前题目为空')
            self.close()
            return None
        self.xianshitimu()
        self.label.setText('共'+str(len(self.questionresall))+'题')
        self.init_collectbutton()

        session.close()



    def tijiaodaan(self):

        Session = sessionmaker(bind=engine)
        session = Session()
        questionid=self.questionresall[0][0]
        if self.questionnowid<len(self.questionresall):
            questionid= self.questionresall[self.questionnowid][0]
        questionres = session.query(question).filter(
            and_(question.id ==questionid , question.course_name == self.coursename)).first()

        userdaan = ""
        if questionres.questionType == 'xz':

            qlist = self.findChildren(QtWidgets.QRadioButton)
            tempkey=['A','B','C','D','E','F','G','H']
            num=0
            for i in qlist:
                name=i.isChecked()
                if name:
                    userdaan+=tempkey[int(num)]
                num+=1


        elif questionres.questionType == 'pd':

            qlist = self.findChildren(QtWidgets.QRadioButton)
            tempkey = ['True', 'False']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1


        elif questionres.questionType == 'mxz':

            qlist = self.findChildren(QtWidgets.QCheckBox)
            tempkey = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            num = 0
            for i in qlist:
                name = i.isChecked()
                if name:
                    userdaan += tempkey[int(num)]
                num += 1


        elif questionres.questionType == 'tk':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan=i.toPlainText()
        elif questionres.questionType == 'jd':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan = i.toPlainText()
        elif questionres.questionType == 'mcjs':

            qlist = self.findChildren(QtWidgets.QTextEdit)
            for i in qlist:
                userdaan = i.toPlainText()
        #考试模式
        if self.xunlianmoshi==1:
            if userdaan!='':
                session.query(tempuserans).filter(tempuserans.question_id == questionid).delete()
                tempuseran = tempuserans()
                tempuseran.question_id = questionid
                tempuseran.userans = userdaan
                session.add(tempuseran)
                session.commit()
            # self.xiayiti()

        anser=questionres.answer

        self.label_2.setText("正确答案为："+anser+"   我的答案："+userdaan)



        #错题写入
        if anser!=userdaan:
            session.query(Errors).filter(Errors.errorid == questionid).delete()
            errors = Errors()
            errors.errorid = questionid
            errors.userid = self.current_username
            session.add(errors)
            session.commit()
        # 错题删除
        if self.xunlianmoshi == 2:
            if anser==userdaan:
                session.query(Errors).filter(Errors.errorid == questionid).delete()

                session.commit()
        session.close()

    def shuaxingtihao(self):
        checkboxname = "tihao" + str(self.questionnowid+1)
        qlist = self.findChildren(QtWidgets.QPushButton,checkboxname)
        for i in  qlist:
           i.setStyleSheet("background-color: green")

    def shangyiti(self):

        try:
            self.questionnowid-=1

            # self.changetihao()
            self.xianshitimu()
            self.label_2.setText('')
            if self.questionnowid <= len(self.questionresall) - 1:
                self.pushButton_2.setHidden(False)
            if self.questionnowid <= 0:
                self.pushButton.setHidden(True)
        except:
            QMessageBox.information(self, '提示', '跳转题号超出范围')
            return None
        self.init_collectbutton()
    def inittempuser(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        from model.question import tempuserans
        session.query(tempuserans).filter().delete()
        session.commit()
        session.close()
    def xiayiti(self):
        try:
            self.questionnowid += 1
            # self.changetihao()
            self.xianshitimu()
            self.label_2.setText('')

            if self.questionnowid >= len(self.questionresall)-1:
                self.pushButton_2.setHidden(True)
            if self.questionnowid > 0:
                self.pushButton.setHidden(False)
        except:
            QMessageBox.information(self, '提示', '跳转题号超出范围')
            return None

        self.init_collectbutton()

    def xianshitimu(self):
        #题目内容


        from controllers.utils.displayques import displayques
        questionid = self.questionresall[self.questionnowid][0]
        papernum=len(self.questionresall)
        display = displayques(self,self.textBrowser_2, self.gridtalLayout1, questionid,self.coursename,self.questionnowid,papernum,None,self.pushButton_4)
        display.display()
        self.showMaximized()



    # def changetihao(self):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     questionall = session.query(question.id).filter(
    #         question.course_name == self.coursename).all()
    #     try:
    #
    #         self.questionnowid = questionall[self.nowid - 1].id
    #     except:
    #         QtWidgets.QMessageBox.information(self, '题号', '超出题目范围')
    #     session.close()
        # self.lineEdit.setText(str(self.nowid))


    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '训练',
                                               "是否要退出训练？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()

    # def inittihaodisplay(self):
    #     papernum = len(self.questionresall)
    #     rownum=papernum//25+1
    #     clonum=25
    #     tihao=1
    #     for i in range(rownum):
    #         for j in range(clonum):
    #             if tihao > papernum:
    #                 break
    #             checkboxname = "tihao" + str(tihao)
    #             checkbox = QtWidgets.QPushButton()
    #             checkbox.setFixedSize(60,25)
    #
    #             checkbox.setObjectName(checkboxname)
    #             checkbox.setText(str(tihao))
    #             self.tihaolayout.addWidget(checkbox, i,j)
    #
    #             checkbox.clicked.connect(partial(self.jumptihao, checkbox.text()))
    #             tihao += 1
    def jumptihao(self,buttext):
        self.questionnowid=int(buttext)-1
        self.xianshitimu()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        modelutil = ModelUtil()
        modelutil.inittempuser()