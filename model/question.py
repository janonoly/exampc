from sqlalchemy import Column, Integer, String, ForeignKey, Text
from model.createdb import Base
from sqlalchemy_utils.types.choice import ChoiceType


class courselist(Base):
  __tablename__ = "courselist"
  id = Column(Integer, primary_key=True, autoincrement=True)
  coursename = Column(String(255))
  leibiename = Column(String(255))


  def __repr__(self):
    return "<courselist( name='%s')>" % (
       self.coursename)


class question(Base):
  __tablename__ = "question"
  Question_TYPES = [
    (u'xz', u'单选题'),
    (u'pd', u'判断题'),
    (u'mxz', u'多选题'),
    (u'jd', u'填空题')
  ]
  id = Column(Integer, primary_key=True,autoincrement=True)
  course_name= Column(String(255), ForeignKey("courselist.coursename"),name=u"考试科目" )
  questionType = Column(ChoiceType(Question_TYPES), default="xz", name=u"题目类型")
  content =Column(Text,name=u"题目内容")
  answer =Column(Text,name=u"正确答案")
  zhangjie =Column(Integer,name=u"章节",default=1)
  choice_a =Column(Text,name=u"A选项", default="A.")
  choice_b =Column(Text,name=u"B选项", default="B.")
  choice_c =Column(Text,name=u"C选项", default="C.")
  choice_d =Column(Text,name=u"D选项", default="D.")
  choice_e =Column(Text,name=u"E选项", default="E.")
  choice_f =Column(Text,name=u"F选项", default="F.")




class PaperList(Base):#用于查看往期考试题目可能不用
    __tablename__ = "paperList"

    course_name = Column(String(255) , primary_key=True)
    name = Column(String(255), name=u"试卷名", default=u"")
    single_choice_num = Column(Integer, name=u"单选题数", default=40)
    single_choice_score = Column(Integer, name=u"单选分值", default=1)
    judgment = Column(Integer, name=u"判断题数", default=20)
    judgment_score = Column(Integer, name=u"判断分值", default=1)
    multiple_choice_num = Column(Integer, name=u"多选题数", default=20)
    multiple_choice_score = Column(Integer, name=u"多选分值", default=1)
    jd_choice_num = Column(Integer, name=u"填空题数", default=20)
    jd_choice_score = Column(Integer, name=u"填空分值", default=1)
    kaoshishijian=Column(Integer, name=u"考试时间", default=60)

class tempuserans(Base):
  __tablename__ = "tempuserans"

  userans = Column(String(255),name=u"用户答案", default="")
  question_id = Column(Integer, primary_key=True)




