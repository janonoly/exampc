import random
from sqlalchemy.orm import sessionmaker

from model.createdb import engine

class createpaper(object):
    def __init__(self,coursename,zhangjie=None):
        self.coursename=coursename
        self.zhangjie = zhangjie

    def createpaper(self):
        Session = sessionmaker(bind=engine)
        # 每次执行数据库操作时，都需要创建一个session
        session = Session()
        from model.question import  PaperList,question
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

            from sqlalchemy import and_
            question_id_list=[]
            question_id_listxz=[]
            question_id_listpd =[]
            question_id_listmxz=[]
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
                if len(xz_listmxz) > paperlist.judgment:
                    question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)
                xz_listjd = session.query(question.id).filter(
                    and_(question.questionType == 'jd', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listjd) > paperlist.judgment:
                    question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)
                kssj = paperlist.kaoshishijian
                # 试卷题号集合与考试时间
                question_id_list = question_id_listxz + question_id_listpd + question_id_listmxz + question_id_listjd
                question_id_list.append(kssj)
            else:

                xz_listxz = session.query(question.id).filter(and_(question.questionType == 'xz', question.course_name == coursename)).all()
                question_id_listxz = random.sample(xz_listxz, paperlist.single_choice_num)
                xz_listpd = session.query(question.id).filter(and_(question.questionType == 'pd', question.course_name == coursename)).all()
                question_id_listpd = random.sample(xz_listpd, paperlist.judgment)
                xz_listmxz = session.query(question.id).filter(and_(question.questionType == 'mxz', question.course_name == coursename)).all()
                question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)
                xz_listjd = session.query(question.id).filter(and_(question.questionType == 'jd', question.course_name == coursename)).all()
                question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)
                kssj = paperlist.kaoshishijian
                #试卷题号集合与考试时间
                question_id_list=question_id_listxz+question_id_listpd+question_id_listmxz+question_id_listjd
                question_id_list.append(kssj)
            session.commit()
            return question_id_list
        except:
            pass
        finally:
            session.close()



