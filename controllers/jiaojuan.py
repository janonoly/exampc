from PyQt5.QtWidgets import QWidget
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from views.jiaojuan import Ui_Dialog
from model.createdb import engine
from model.question import tempuserans,question
class juaojuan(QWidget,Ui_Dialog):
    def __init__(self,paperlist,course):
        super().__init__()
        self.setupUi(self)
        self.course=course
        self.questionidlist=paperlist
        self.jishuadefen()



    def jishuadefen(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        yemian=""
        xzyemian=''
        pdyemian = ''
        mxzyemian = ''
        jdyemian = ''

        tihao=1
        xzdaduitishu=0
        pddaduitishu = 0
        mxzdaduitishu = 0
        jddaduitishu = 0
        for que in self.questionidlist:

            usrans = session.query(tempuserans).filter(tempuserans.question_id == que[0]).first()
            # rightans=session.query(question).filter(and_(question.id==usrans.question_id),(question.questionType=='xz')).first()
            rightans = session.query(question).filter(question.id ==que[0]).first()
            if rightans.questionType=='xz':
                useranss=''
                if usrans is not None :
                    if  rightans.answer==usrans.userans:
                        xzdaduitishu+=1
                        useranss=usrans.userans
                        xzyemian+=str(tihao)+':'+rightans.content+'正确答案(%s)'% rightans.answer+'我的答案(%s)'%useranss+'\n'
                        xzyemian = "<font color='black'>" + xzyemian + "</font><br>"
                    else:
                        xzyemian += str(
                            tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                        xzyemian = "<font color='red'>" + xzyemian + "</font><br>"
                else:
                    xzyemian += str(
                        tihao) +':'+ rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                    xzyemian = "<font color='red'>" + xzyemian + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_a + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_b + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_c + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_d + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_e + "</font><br>"
                xzyemian += "<font color='black'>" + rightans.choice_f + "</font><br>"
            elif  rightans.questionType=='pd':
                useranss = ''
                if usrans is not None:
                    if rightans.answer == usrans.userans:
                        pddaduitishu += 1
                        useranss = usrans.userans
                        pdyemian+=str(tihao)+':'+rightans.content+'正确答案(%s)'% rightans.answer+'我的答案(%s)'%useranss+'\n'
                        pdyemian = "<font color='black'>" + pdyemian + "</font><br>"
                    else:
                        pdyemian += str(
                            tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                        pdyemian = "<font color='red'>" + pdyemian + "</font><br>"
                else:
                    pdyemian += str(
                        tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                    pdyemian = "<font color='red'>" + pdyemian + "</font><br>"
            elif  rightans.questionType == 'mxz':
                useranss = ''
                if usrans is not None:
                    if rightans.answer == usrans.userans:
                        mxzdaduitishu += 1
                        useranss = usrans.userans
                        mxzyemian += str(
                            tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                        mxzyemian = "<font color='black'>" + mxzyemian + "</font><br>"
                    else:
                        mxzyemian += str(
                            tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                        mxzyemian = "<font color='red'>" + mxzyemian + "</font><br>"
                else:
                    mxzyemian += str(
                        tihao) +':'+ rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                    mxzyemian = "<font color='red'>" + mxzyemian + "</font><br>"

                mxzyemian +=  "<font color='black'>" + rightans.choice_a + "</font><br>"
                mxzyemian += "<font color='black'>" + rightans.choice_b + "</font><br>"
                mxzyemian += "<font color='black'>" + rightans.choice_c + "</font><br>"
                mxzyemian += "<font color='black'>" + rightans.choice_d+ "</font><br>"
                mxzyemian += "<font color='black'>" + rightans.choice_e + "</font><br>"
                mxzyemian += "<font color='black'>" + rightans.choice_f + "</font><br>"
            elif   rightans.questionType == 'jd':
                useranss = ''
                if usrans is not None:
                    if rightans.answer == usrans.userans:
                        jddaduitishu += 1
                        useranss = usrans.userans
                        jdyemian+=str(tihao)+rightans.content+'正确答案(%s)'% rightans.answer+'我的答案(%s)'%useranss+'\n'
                        jdyemian="<font color='black'>"+jdyemian+"</font><br>"
                    else:
                        jdyemian += str(
                            tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                        jdyemian = "<font color='red'>" + jdyemian + "</font><br>"
                else:
                    jdyemian += str(
                        tihao)+':' + rightans.content + '正确答案(%s)' % rightans.answer + '我的答案(%s)' % useranss + '\n'
                    jdyemian = "<font color='red'>" + jdyemian + "</font><br>"

            # yemian+=rightans.content+'正确答案(%s)'% rightans.answer+'我的答案(%s)'%usrans.userans+'\n'
            # yemian+=question.choice_a+'\n'
            # yemian += question.choice_a + '\n'
            # yemian += question.choice_a + '\n'
            # yemian += question.choice_a + '\n'

            tihao+=1
        from model.question import PaperList
        paperset = session.query(PaperList).filter(PaperList.course_name== self.course).first()
        xzfen=paperset.single_choice_score
        pdfen=paperset.judgment_score
        mxzfen=paperset.multiple_choice_score
        jdfen=paperset.jd_choice_score
        xzdaduitishufen= xzfen*xzdaduitishu
        pddaduitishufen = pdfen*pddaduitishu
        mxzdaduitishufen = mxzfen*mxzdaduitishu
        jddaduitishufen = jdfen*jddaduitishu
        zhongfen=xzdaduitishufen+pddaduitishufen+mxzdaduitishufen+jddaduitishufen
        zhongfenstr="<font size='6' color='red'>" +'总分:'+ str(zhongfen) + "</font><br>"
        xzcuotistr="<font size='4' color='red'>" + '选择题数：%s ' % paperset.single_choice_num+'答对题数：%s' % xzdaduitishu + "</font><br>"
        pdcuotistr = "<font size='4' color='red'>" + '选择题数：%s ' % paperset.judgment+'答对题数：%s' % pddaduitishu  + "</font><br>"
        mxzcuotistr = "<font size='4' color='red'>" + '选择题数：%s ' % paperset.multiple_choice_num+ '答对题数：%s' % mxzdaduitishu  + "</font><br>"
        jdcuotistr = "<font size='4' color='red'>" + '选择题数：%s ' % paperset.jd_choice_num + '答对题数：%s' % jddaduitishu  + "</font><br>"

        yemian=zhongfenstr+xzcuotistr+xzyemian+pdcuotistr+pdyemian+mxzcuotistr+mxzyemian+jdcuotistr+jdyemian
        # yemian =zhongfenstr+ xzyemian  + pdyemian + mxzyemian  + jdyemian

        # self.textBrowser.setHtml("<font color='red'>hell</font>")
        self.textBrowser.setHtml(yemian)














