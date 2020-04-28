from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from controllers.utils.loginutil import CommonUtil
from controllers.utils.modeutil import ModelUtil
from views.jiaojuan import Ui_Dialog
from model.createdb import engine
from model.question import tempuserans,question
class juaojuan(QWidget,Ui_Dialog):
    def __init__(self,paperlist,course,curentusername,xunlianmoshi):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(CommonUtil.APP_ICON))
        self.course=course
        self.curentusername=curentusername
        self.questionidlist=paperlist
        self.xunlianmoshi = xunlianmoshi
        self.jishuadefen()



    def jishuadefen(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        yemian=""
        tkyemian = ''
        pdyemian = ''
        xzyemian = ''
        mxzyemian = ''
        mcjsyemian = ''
        jdyemian = ''

        tihao=1
        xzdaduitishu=0
        pddaduitishu = 0
        mxzdaduitishu = 0
        tkdaduitishu = 0
        jddaduitishu = 0
        mcjsdaduitishu = 0
        xztibool=False
        mxztibool = False
        pdtibool = False
        jdtibool = False
        tktibool = False
        mcjstibool = False

        for que in self.questionidlist:
            usrans = session.query(tempuserans).filter(tempuserans.question_id == que[0]).first()
            # rightans=session.query(question).filter(and_(question.id==usrans.question_id),(question.questionType=='xz')).first()
            rightans = session.query(question).filter(question.id ==que[0]).first()
            if rightans.questionType=='xz':
                xztibool=True
                yemianxz, xzdaduitishu= self.get_jie_xi(usrans, rightans, xzdaduitishu, tihao)
                xzyemian += yemianxz
            elif  rightans.questionType=='pd':
                pdtibool = True
                yemianpd, pddaduitishu = self.get_jie_xi(usrans, rightans, pddaduitishu, tihao)
                pdyemian += yemianpd
            elif  rightans.questionType == 'mxz':
                mxztibool = True

                yemianmxz, mxzdaduitishu = self.get_jie_xi(usrans, rightans, mxzdaduitishu, tihao)
                mxzyemian += yemianmxz
            elif rightans.questionType == 'tk':
                tktibool = True

                yemiantk, tkdaduitishu = self.get_jie_xi(usrans, rightans, tkdaduitishu, tihao)
                tkyemian += yemiantk
            elif   rightans.questionType == 'jd':
                jdtibool = True

                yemianjd, jddaduitishu = self.get_jie_xi(usrans, rightans, jddaduitishu, tihao)
                jdyemian += yemianjd
            elif rightans.questionType == 'mcjs':
                mcjstibool = True

                yemianmcjs, mcjsdaduitishu = self.get_jie_xi(usrans, rightans, mcjsdaduitishu, tihao)
                mcjsyemian += yemianmcjs
            tihao+=1

        from model.question import PaperList
        paperset = session.query(PaperList).filter(PaperList.course_name== self.course).first()
        xzfen=paperset.single_choice_score
        pdfen=paperset.judgment_score
        mxzfen=paperset.multiple_choice_score
        tkfen = paperset.tk_choice_score
        jdfen=paperset.jd_choice_score
        mcjsfen=paperset.mcjs_choice_score
        xzdaduitishufen= xzfen*xzdaduitishu
        pddaduitishufen = pdfen*pddaduitishu
        mxzdaduitishufen = mxzfen*mxzdaduitishu
        tkdaduitishufen = tkfen * tkdaduitishu
        jddaduitishufen = jdfen*jddaduitishu
        mcjsdaduitishufen = mcjsfen * mcjsdaduitishu
        zhongfen=xzdaduitishufen+pddaduitishufen+mxzdaduitishufen+jddaduitishufen+tkdaduitishufen+mcjsdaduitishufen
        zhongfenstr="<font size='6' color='red'>" +'总分:'+ str(zhongfen) + "</font><br>"
        tkcuotistr=''
        xzcuotistr=''
        pdcuotistr = ''
        mxzcuotistr=''
        mcjscuotistr=''
        jdcuotistr=''
        if xztibool:
            xzcuotistr="<font size='4' color='red'>" + '单选题数：%s ' % paperset.single_choice_num+'答对题数：%s' % xzdaduitishu + "</font><br>"
        if pdtibool:
            pdcuotistr = "<font size='4' color='red'>" + '判断题数：%s ' % paperset.judgment+'答对题数：%s' % pddaduitishu  + "</font><br>"
        if mxztibool:
            mxzcuotistr = "<font size='4' color='red'>" + '多选题数：%s ' % paperset.multiple_choice_num+ '答对题数：%s' % mxzdaduitishu  + "</font><br>"
        if tktibool:
            tkcuotistr = "<font size='4' color='red'>" + '填空题数：%s ' % paperset.tk_choice_num + '答对题数：%s' % tkdaduitishu + "</font><br>"
        if mcjstibool:
            mcjscuotistr = "<font size='4' color='red'>" + '名词解释题数：%s ' % paperset.mcjs_choice_num + '答对题数：%s' % mcjsdaduitishu + "</font><br>"
        if jdtibool:
            jdcuotistr = "<font size='4' color='red'>" + '简答题数：%s ' % paperset.jd_choice_num + '答对题数：%s' % jddaduitishu  + "</font><br>"

        yemian=zhongfenstr+tkcuotistr+tkyemian+pdcuotistr+pdyemian+xzcuotistr+xzyemian+mxzcuotistr+mxzyemian+mcjscuotistr+mcjsyemian+jdcuotistr+jdyemian
        # yemian =zhongfenstr+ xzyemian  + pdyemian + mxzyemian  + jdyemian
        # self.textBrowser.setHtml("<font color='red'>hell</font>")
        self.textBrowser.setHtml(yemian)
        session.close()

        #写入得分
        if zhongfen>0:
            if self.xunlianmoshi == 5:
                modelutil=ModelUtil()
                modelutil.save_score(self.curentusername,zhongfen,self.course)
                modelutil.session_close()

    def get_jie_xi(self,usrans, rightans,jddaduitishu,tihao):
        useranss = ''
        mcjsyemian = ''
        if usrans is not None:
            #填空题可能有两个空
            # str1 = ' 填空  是    士大夫 '
            # right_ans = str1.replace(' ', '')

            if rightans.answer.replace(' ', '') == usrans.userans.replace(' ', ''):
                jddaduitishu += 1

                mcjsyemian += str(
                    tihao) + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % usrans.userans + '\n'
                mcjsyemian = "<font color='black'>" + mcjsyemian + "</font><br>"
            else:
                mcjsyemian += str(
                    tihao) + ':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % usrans.userans + '\n'
                mcjsyemian = "<font color='red'>" + mcjsyemian + "</font><br>"
        else:
            mcjsyemian += str(
                tihao) + ':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
            mcjsyemian = "<font color='red'>" + mcjsyemian + "</font><br>"
        if len(rightans.choice_a)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_a + "</font><br>"
        if len(rightans.choice_b)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_b + "</font><br>"
        if len(rightans.choice_c)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_c + "</font><br>"
        if len(rightans.choice_d)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_d + "</font><br>"
        if len(rightans.choice_e)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_e + "</font><br>"
        if len(rightans.choice_f)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_f + "</font><br>"
        if len(rightans.choice_g)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_g + "</font><br>"
        if len(rightans.choice_h)>2:
            mcjsyemian += "<font color='black'>" + rightans.choice_h + "</font><br>"
        return mcjsyemian, jddaduitishu
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """

        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            modelutil=ModelUtil()
            modelutil.inittempuser()
            event.accept()
        else:
            event.ignore()













