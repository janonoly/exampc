import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from model.createdb import Base, engine


# 定义映射类User，其继承上一步创建的Base
class user(Base):
  # 指定本类映射到users表
  __tablename__ = 'user'

  # 指定id映射到id字段; id字段为整型，为主键
  id = Column(Integer, primary_key=True, autoincrement=True)
  # 指定name映射到name字段; name字段为字符串类形，
  name = Column(String(32))
  password = Column(String(32))






# 定义映射类User，其继承上一步创建的Base
class Errors(Base):
  # 指定本类映射到users表
  __tablename__ = 'errors'

  # 指定id映射到id字段; id字段为整型，为主键
  id = Column(Integer, primary_key=True, autoincrement=True)
  # 指定name映射到name字段; name字段为字符串类形，
  userid = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), name=u"用户id" )
  errorid = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'), name=u"错题id" )

# 定义映射类User，其继承上一步创建的Base
class Collects(Base):
  # 指定本类映射到users表
  __tablename__ = 'collects'

  # 指定id映射到id字段; id字段为整型，为主键
  id = Column(Integer, primary_key=True, autoincrement=True)
  # 指定name映射到name字段; name字段为字符串类形，
  userid = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), name=u"用户id")
  collectid = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'), name=u"收集id")



# 定义映射类User，其继承上一步创建的Base
class Scores(Base):
  # 指定本类映射到users表
  __tablename__ = 'scores'

  # 指定id映射到id字段; id字段为整型，为主键
  id = Column(Integer, primary_key=True, autoincrement=True)
  # 指定name映射到name字段; name字段为字符串类形，
  userid = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), name=u"用户id")
  score = Column(Integer, name=u"分数")
  coursename = Column(String(255), ForeignKey('question.id', ondelete='CASCADE'), name=u"考试科目")
  datetime = Column(DateTime, default=datetime.datetime.now,name=u"时间")

