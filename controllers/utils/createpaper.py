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
            # # zhuanyedict = {'数学': ['第一章', '第二章', '第三章'], '英语': ['第三章', '第四章', '第五章']}
                 # dsaf = {'单选题': ['单选题', '0', '0'], '多选题': ['多选题', '0', '0'], '判断题': ['判断题', '0', '0'], '填空题': ['填空题', '0', '0'], '简答题': ['简答题', '0', '0']}
                 #
                 # er={'数学': ['数学', '5'], '英语': ['英语', '5']}
                 # eqrw={'数学': ['四级', '五级'], '英语': ['三级', '四级', '五级']}

                 # dengjilist = ['五级', '四级']
                 # zhuanyetishudict = {'数学': {'xz':1,'mxz':1,'pd':1,'tk':1,'jd':1}, '英语': {'xz':1,'mxz':1,'pd':1,'tk':0,'jd':0}}
                 # # timuleixingshudict = {'单选题': 20, '多选题':20, '判断题': 20, '填空题': 20, '简答题': 20}

           xznum = []
           mxznum = []
           pdnum = []
           tknum = []
           jdnum = []
           mcjsnum = []

           for (k,v) in  self.zhuanyedict.items():
               xzquestion_id = []
               mxzquestion_id = []
               pdquestion_id = []
               tkquestion_id = []
               jdquestion_id = []
               mcjsquestion_id = []
               queryset=session.query(question.id).filter(question.course_name == k)
               if len(v)==0:
                   que = queryset
                   xzquestion_id, mxzquestion_id, pdquestion_id, tkquestion_id, jdquestion_id, mcjsquestion_id = self.gongtong(que,k)
               else:
                   for i in range(len(v)):
                       que = queryset.filter(question.zhangjie == v[i])
                       xzquestion_id1 ,mxzquestion_id1,pdquestion_id1,tkquestion_id1,jdquestion_id1,mcjsquestion_id1=self.gongtong(que,k)
                       xzquestion_id.extend(xzquestion_id1)
                       mxzquestion_id.extend(mxzquestion_id1)
                       pdquestion_id.extend(pdquestion_id1)
                       tkquestion_id.extend(tkquestion_id1)
                       jdquestion_id.extend(jdquestion_id1)
                       mcjsquestion_id.extend(mcjsquestion_id1)

               # shuliang=self.zhuanyetishudict[k]

               zhuanyeshuliangres = self.zhuanyeshuliang(self.zhuanyetishudict,self.timuleixingshudict)
               shuliang=zhuanyeshuliangres[k]
               try:
                   if xzquestion_id:
                       if len(xzquestion_id)>=shuliang['单选题']:
                            xznum.extend(random.sample(xzquestion_id, shuliang['单选题']))
                       else:
                           return '单选题题库数量不够'
                   elif not shuliang['单选题'] == 0:
                       return '单选题题库数量不够'
               except:
                   pass
               try:
                   if mxzquestion_id:
                       if len(mxzquestion_id) >= shuliang['多选题']:
                            mxznum.extend(random.sample(mxzquestion_id, shuliang['多选题']))
                       else:
                           return '单选题题库数量不够'
                   elif not shuliang['多选题'] == 0:
                       return '多选题题库数量不够'
               except:
                   pass
               try:
                   if pdquestion_id:
                       if len(pdquestion_id) >= shuliang['判断题']:
                            pdnum.extend(random.sample(pdquestion_id, shuliang['判断题']))
                       else:
                           return '判断题题库数量不够'
                   elif not shuliang['判断题'] == 0:
                       return '判断题题库数量不够'
               except:
                   pass
               try:
                   if tkquestion_id:
                       if len(tkquestion_id) >= shuliang['填空题']:
                            tknum.extend(random.sample(tkquestion_id, shuliang['填空题']))
                       else:
                           return '填空题题库数量不够'
                   elif not shuliang['填空题']==0:
                       return '填空题题库数量不够'
               except:
                   pass
               try:
                   if jdquestion_id:
                       if len(jdquestion_id) >= shuliang['简答题']:
                            jdnum.extend(random.sample(jdquestion_id, shuliang['简答题']))
                       else:
                           return '简答题题库数量不够'
                   elif not shuliang['简答题'] == 0:
                       return '简答题题库数量不够'
               except:
                   pass
               try:
                   if mcjsquestion_id:
                       if len(mcjsquestion_id) >= shuliang['名词解释']:
                           mcjsnum.extend(random.sample(mcjsquestion_id, shuliang['名词解释']))
                       else:
                           return '名词解释题库数量不够'
                   elif not shuliang['名词解释']==0:
                       return  '名词解释题库数量不够'
               except:
                   pass
           question_id_list = xznum + mxznum + pdnum + tknum + jdnum +mcjsnum
           return question_id_list
        except:
            return '出题失败'
        finally:
            session.close()
    def zhuanyeshuliang(self,zhuanyetishudict,timuleixingshudict):
        # zhuanyetishudict={'战伤救护': ['战伤救护', '47'],'数学': ['数学', '53']}
        # timuleixingshudict={'单选题': 20, '多选题': 20, '判断题': 20, '填空题': 20, '简答题': 20}

        zhongtishu=0
        for (k,v) in zhuanyetishudict.items():
            tishu = int(zhuanyetishudict[k][1])
            zhongtishu+=tishu
        zhuanyetishubaifenbi={}
        for (k, v) in zhuanyetishudict.items():
            tishu = int(zhuanyetishudict[k][1])
            zhuanyetishubaifenbi[k]=tishu/zhongtishu
        timuxiangqing={}
        for (k, v) in zhuanyetishudict.items():
            dangetimu={}
            for (j,s) in timuleixingshudict.items():
                baifenbi = zhuanyetishubaifenbi[k]
                timuleixingshuliang = timuleixingshudict[j]
                dangetimu[j] = int(timuleixingshuliang*baifenbi)
            timuxiangqing[k]=dangetimu
        shengchengzhongshu ={}
        for (k, v) in timuxiangqing.items():
            timushuliang = timuxiangqing[k]
            dankezhonghsu=0
            for (j, s) in timushuliang.items():
                dankezhonghsu+=timushuliang[j]
            shengchengzhongshu[k]=dankezhonghsu
        queshaodict={}
        flag=0
        for (k,v) in zhuanyetishudict.items():
            queshao = int(zhuanyetishudict[k][1])-shengchengzhongshu[k]
            queshaodict[k]=queshao
            breknum=0
            breaknum2=0
            for (j,s) in timuxiangqing[k].items():
                if queshao:
                    breknum += 1
                    if breknum>flag:
                        timuxiangqing[k][j]+=1
                        flag+=1
                        breaknum2+=1
                        if breaknum2>=queshao:
                            break
        zuizhong=timuxiangqing





        return zuizhong
    def gongtong(self,que,zhuanyename):
        xzquestion_id = []
        mxzquestion_id = []
        pdquestion_id = []
        tkquestion_id = []
        jdquestion_id = []
        mcjsquestion_id = []
        for j in range(len(self.dengjilist[zhuanyename])):
            xzque1 = que.filter(and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'xz')).all()

            xzquestion_id.extend(xzque1)
            mxzque1 = que.filter(and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'mxz')).all()
            mxzquestion_id.extend(mxzque1)
            pdque1 = que.filter(
                and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'pd')).all()
            pdquestion_id.extend(pdque1)
            tkque1 = que.filter(
                and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'tk')).all()
            tkquestion_id.extend(tkque1)
            jdque1 = que.filter(
                and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'jd')).all()
            jdquestion_id.extend(jdque1)
            mcjsque1 = que.filter(
                and_(question.dengji == self.dengjilist[zhuanyename][j], question.questionType == 'mcjs')).all()
            mcjsquestion_id.extend(jdque1)
        return  xzquestion_id ,mxzquestion_id,pdquestion_id,tkquestion_id,jdquestion_id,mcjsquestion_id


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


            question_id_list=[]
            question_id_listxz=[]
            question_id_listpd =[]
            question_id_listmxz=[]
            question_id_listtk = []
            question_id_listjd=[]
            question_id_listmcjs=[]
            if self.zhangjie:
                xz_listxz = session.query(question.id).filter(
                    and_(question.questionType == 'xz', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()

                if len(xz_listxz)>=paperlist.single_choice_num:
                    question_id_listxz = random.sample(xz_listxz, paperlist.single_choice_num)

                xz_listpd = session.query(question.id).filter(
                    and_(question.questionType == 'pd', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listpd) >= paperlist.judgment:
                     question_id_listpd = random.sample(xz_listpd, paperlist.judgment)

                xz_listmxz = session.query(question.id).filter(
                    and_(question.questionType == 'mxz', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listmxz) >= paperlist.multiple_choice_num:
                    question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)

                xz_listjd = session.query(question.id).filter(
                    and_(question.questionType == 'jd', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listjd) >= paperlist.jd_choice_num:
                    question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)

                xz_listtk = session.query(question.id).filter(
                    and_(question.questionType == 'tk', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listtk) >= paperlist.tk_choice_num:
                    question_id_listtk = random.sample(xz_listtk, paperlist.tk_choice_num)

                xz_listmcjs = session.query(question.id).filter(
                    and_(question.questionType == 'mcjs', question.course_name == coursename,
                         question.zhangjie == self.zhangjie)).all()
                if len(xz_listmcjs) >=paperlist.mcjs_choice_num:
                    question_id_listmcjs = random.sample(xz_listmcjs, paperlist.mcjs_choice_num)

                kssj = paperlist.kaoshishijian
                # 试卷题号集合与考试时间
                question_id_list = question_id_listxz + question_id_listpd + question_id_listmxz +question_id_listtk+ question_id_listjd+question_id_listmcjs
                question_id_list.append(kssj)
            else:

                xz_listxz = session.query(question.id).filter(and_(question.questionType == 'xz', question.course_name == coursename)).all()

                if len(xz_listxz) >= paperlist.single_choice_num:
                    question_id_listxz = random.sample(xz_listxz, paperlist.single_choice_num)
                xz_listpd = session.query(question.id).filter(and_(question.questionType == 'pd', question.course_name == coursename)).all()
                if len(xz_listpd) >= paperlist.judgment:
                    question_id_listpd = random.sample(xz_listpd, paperlist.judgment)
                xz_listmxz = session.query(question.id).filter(and_(question.questionType == 'mxz', question.course_name == coursename)).all()
                if len(xz_listmxz) >= paperlist.multiple_choice_num:
                    question_id_listmxz = random.sample(xz_listmxz, paperlist.multiple_choice_num)
                xz_listjd = session.query(question.id).filter(and_(question.questionType == 'jd', question.course_name == coursename)).all()
                if len(xz_listjd) >= paperlist.jd_choice_num:
                    question_id_listjd = random.sample(xz_listjd, paperlist.jd_choice_num)

                xz_listtk = session.query(question.id).filter(
                    and_(question.questionType == 'tk', question.course_name == coursename)).all()
                if len(xz_listtk) >= paperlist.tk_choice_num:
                    question_id_listtk = random.sample(xz_listtk, paperlist.tk_choice_num)

                xz_listmcjs = session.query(question.id).filter(
                    and_(question.questionType == 'mcjs', question.course_name == coursename)).all()
                if len(xz_listmcjs) >= paperlist.mcjs_choice_num:
                    question_id_listmcjs = random.sample(xz_listmcjs, paperlist.mcjs_choice_num)
                kssj = paperlist.kaoshishijian

                #试卷题号集合与考试时间
                question_id_list=question_id_listxz+question_id_listpd+question_id_listmxz+question_id_listtk+question_id_listjd+question_id_listmcjs
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

