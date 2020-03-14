from PyQt5.QtWidgets import QMessageBox
from sqlalchemy import and_, distinct, or_
from sqlalchemy.orm import sessionmaker

from model.createdb import engine
from model.user import user, Collects, Scores
from model.question import courselist,question


class ModelUtil(object):
    Session = sessionmaker(bind=engine)
    # 每次执行数据库操作时，都需要创建一个session
    session = Session()
    def getuserinstance(self,current_username):

        usercurrent = self.session.query(user.id).filter(user.name == current_username).first()
        return usercurrent

    def save_collect(self,collect):
        collect_instance = self.session.query(Collects).filter(and_(Collects.collectid == collect.collectid,Collects.userid ==collect.userid))
        if collect_instance.count()>=1:
            for i in collect_instance:
                self.session.delete(i)
            self.session.commit()
            return False
        else:
            self.session.add(collect)
            self.session.commit()
            return True
    def save_score(self,userid,totolscore,course):
        score=Scores()
        score.userid=userid
        score.score=totolscore
        score.coursename=course
        self.session.add(score)
        self.session.commit()

    def get_score(self, userid):


        coursename = self.session.query(Scores.coursename).filter(Scores.userid == userid).distinct(Scores.coursename)
        col=coursename.count()
        # dataTable = [
        #     ["PTSA", 130, 182, 120, 154, 109, 170, 110, 150, 132, 141, 114, 100, 160],
        # ]

        dataTable=[]
        for i in range(col):
            curentcorsename=coursename[i].coursename
            res = self.session.query(Scores).filter(Scores.userid == userid,Scores.coursename==curentcorsename)
            rows = res.count()
            # score_list = [[0 for i in range(rows + 1)] ]
            score_list=[]
            score_list.append(curentcorsename)
            num=1

            for i in res:
                # score_list[num] = i.score
                score_list.append(i.score)
                # score_list[1][num] = i.datetime
                num += 1

            dataTable.append(score_list)

        return dataTable

    def inittempuser(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        from model.question import tempuserans
        # result = session.query(tempuserans).all()
        # session.delete(result)
        session.query(tempuserans).filter().delete()
        session.commit()
        session.close()
    def get_collect(self,collect):
        collect_instance = self.session.query(Collects).filter(
            and_(Collects.collectid == collect.collectid, Collects.userid == collect.userid))
        if collect_instance.count() >= 1:

            return True
        else:

            return False
    def get_zhuaye_kemu_dengji(self,selected_zhuanye_kemudict):



        zhuanye_kemu_dengji= {}

        for (k,v) in selected_zhuanye_kemudict.items():
            dengji = []
            if len(v)==0:
                v=['']


            for i in range(len(v)):
                dengjilist = self.session.query(question.dengji).filter(
                    and_(question.course_name ==k,question.zhangjie==v[i] )).distinct(
                    question.dengji).all()
                for i in range(len(dengjilist)):
                    if not dengjilist[i].dengji=='':
                       dengji.insert(0,dengjilist[i].dengji)
            dengji = list(set(dengji))

            zhuanye_kemu_dengji[k]=dengji



        return zhuanye_kemu_dengji
    def get_zhuaye_kemu(self):

        coursename = self.session.query(courselist.coursename).filter().distinct(courselist.coursename).all()
        col = len(coursename)
        # dataTable = [
        #     ["PTSA", 130, 182, 120, 154, 109, 170, 110, 150, 132, 141, 114, 100, 160],
        # ]

        zhuanye_kemu= {}
        for i in range(col):
            curentcorsename = coursename[i].coursename
            kemu = self.session.query(question.zhangjie).filter(question.course_name == curentcorsename).distinct(question.zhangjie).all()
            rows = len(kemu)
            # score_list = [[0 for i in range(rows + 1)] ]

            kemulist=[]
            for j in range(rows):
                # score_list[num] = i.score
                if not kemu[j].zhangjie=='':
                    kemulist.append(kemu[j].zhangjie)
            zhuanye_kemu[curentcorsename]=kemulist

        return zhuanye_kemu
    def get_timuleixing(self,zhuanye_kemudict):
        questiontype=[]
        for (k,v) in zhuanye_kemudict.items():
            questiontype1 = self.session.query(question.questionType).filter(question.course_name==k).distinct(question.questionType).all()
            for i in range(len(questiontype1)):
                questiontype.append(questiontype1[i].questionType.value)
        questiontype=list(set(questiontype))
        return questiontype
    def session_close(self):
        self.session.close()
