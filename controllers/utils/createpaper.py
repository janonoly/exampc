import random
from sqlalchemy.orm import sessionmaker
from model.question import  PaperList,question
from model.createdb import engine
from sqlalchemy import and_

class random_createpaper(object):
    def __init__(self,zhuanyedict,dengjilist,zhuanyetishudict,timuleixingshudict):
        self.zhuanyedict = zhuanyedict
        self.dengjilist = dengjilist
        self.zhuanyetishudict = zhuanyetishudict
        self.timuleixingshudict = timuleixingshudict


    def create_random_paper(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()

        try:
           # xz_mcourse_question_id={}
           # mx_mcourse_zquestion_id = {}
           # pd_mcourse_question_id = {}
           # tk_mcourse_question_id = {}
           # jd_mcourse_question_id = {}
           xznum = []
           mxznum = []
           pdnum = []
           tknum = []
           jdnum = []

           for (k,v) in  self.zhuanyedict.items():
               xzquestion_id = []
               mxzquestion_id = []
               pdquestion_id = []
               tkquestion_id = []
               jdquestion_id = []
               queryset=session.query(question.id).filter(question.course_name == k)
               for i in range(len(v)):
                   que = queryset.filter(question.zhangjie == v[i])
                   for i in range(len(self.dengjilist)):
                       xzque1 = que.filter(and_(question.dengji == self.dengjilist[i],question.questionType=='xz')).all()

                       xzquestion_id.extend(xzque1)
                       mxzque1 = que.filter(and_(question.dengji == self.dengjilist[i], question.questionType == 'mxz')).all()
                       mxzquestion_id.extend(mxzque1)
                       pdque1 = que.filter(
                           and_(question.dengji == self.dengjilist[i], question.questionType == 'pd')).all()
                       pdquestion_id.extend(pdque1)
                       tkque1 = que.filter(
                           and_(question.dengji == self.dengjilist[i], question.questionType == 'tk')).all()
                       tkquestion_id.extend(tkque1)
                       jdque1 = que.filter(
                           and_(question.dengji == self.dengjilist[i], question.questionType == 'jd')).all()
                       jdquestion_id.extend(jdque1)

               shuliang=self.zhuanyetishudict[k]

               xznum.extend(random.sample(xzquestion_id, shuliang['xz']))
               mxznum.extend(random.sample(mxzquestion_id, shuliang['mxz']))
               pdnum.extend(random.sample(pdquestion_id, shuliang['pd']))
               tknum.extend(random.sample(tkquestion_id, shuliang['tk']))
               jdnum.extend(random.sample(jdquestion_id, shuliang['jd']))

           question_id_list = xznum + mxznum + pdnum + tknum + jdnum
           return question_id_list
        except:
            return None
        finally:
            session.close()


class createpaper(object):
    def __init__(self,coursename,zhangjie=None):
        self.coursename=coursename
        self.zhangjie = zhangjie

    def createpaper(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()

        coursename = self.coursename
        try:
            paperlist = session.query(PaperList).filter(PaperList.course_name == coursename).first()
            #根据试卷设置生成试卷
            # sgn=paperlist.single_choice_num
            # sgs=paperlist.single_choice_score
            # pdn=paperlist.judgment
            # pds=paperlist.judgment_score
            # mxzn=paperlist.multiple_choice_num
            # mxzs=paperlist.multiple_choice_score
            # jdn=paperlist.jd_choice_num
            # jds=paperlist.jd_choice_score
            # kssj=paperlist.kaoshishijian


            question_id_list=[]
            question_id_listxz=[]
            question_id_listpd =[]
            question_id_listmxz=[]
            question_id_listtk = []
            question_id_listjd=[]
            if self.zhangjie:
                xz_listxz = session.query(question.id).filter(
                    and_(question.questionType == 'xz', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()

                if len(xz_listxz)>paperlist.single_choice_num:
                    question_id_listxz = random.sample(xz_listxz, paperlist.single_choice_num)

                xz_listpd = session.query(question.id).filter(
                    and_(question.questionType == 'pd', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listpd) > paperlist.judgment:
                     question_id_listpd = random.sample(xz_listpd, paperlist.judgment)

                xz_listmxz = session.query(question.id).filter(
                    and_(question.questionType == 'mxz', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listmxz) > paperlist.multiple_choice_num:
                    question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)

                xz_listjd = session.query(question.id).filter(
                    and_(question.questionType == 'jd', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listjd) > paperlist.jd_choice_num:
                    question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)

                xz_listtk = session.query(question.id).filter(
                    and_(question.questionType == 'tk', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listtk) > paperlist.tk_choice_num:
                    question_id_listtk = random.sample(xz_listtk, paperlist.tk_choice_num)

                kssj = paperlist.kaoshishijian
                # 试卷题号集合与考试时间
                question_id_list = question_id_listxz + question_id_listpd + question_id_listmxz +question_id_listtk+ question_id_listjd
                question_id_list.append(kssj)
            else:

                xz_listxz = session.query(question.id).filter(and_(question.questionType == 'xz', question.course_name == coursename)).all()
                if len(xz_listxz) > paperlist.single_choice_num:
                    question_id_listxz = random.sample(xz_listxz, paperlist.single_choice_num)
                xz_listpd = session.query(question.id).filter(and_(question.questionType == 'pd', question.course_name == coursename)).all()
                if len(xz_listpd) > paperlist.judgment:
                    question_id_listpd = random.sample(xz_listpd, paperlist.judgment)
                xz_listmxz = session.query(question.id).filter(and_(question.questionType == 'mxz', question.course_name == coursename)).all()
                if len(xz_listmxz) > paperlist.multiple_choice_num:
                    question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)
                xz_listjd = session.query(question.id).filter(and_(question.questionType == 'jd', question.course_name == coursename)).all()
                if len(xz_listjd) > paperlist.jd_choice_num:
                    question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)

                xz_listtk = session.query(question.id).filter(
                    and_(question.questionType == 'tk', question.course_name == coursename)).all()
                if len(xz_listtk) > paperlist.tk_choice_num:
                    question_id_listtk = random.sample(xz_listtk, paperlist.tk_choice_num)

                kssj = paperlist.kaoshishijian
                #试卷题号集合与考试时间
                question_id_list=question_id_listxz+question_id_listpd+question_id_listmxz+question_id_listtk+question_id_listjd
                question_id_list.append(kssj)
            session.commit()
            return question_id_list
        except:
            pass
        finally:
            session.close()

    def createpaperformat(self,startid,endid):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()

        coursename = self.coursename
        try:
            questionall_course = session.query(question.id).filter(
                 question.course_name == coursename).all()
            return questionall_course[startid:endid]


        except:
            pass
        session.close()

