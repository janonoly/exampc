from sqlalchemy import Column, Integer, String
from model.createdb import Base


# 定义映射类User，其继承上一步创建的Base
class user(Base):
  # 指定本类映射到users表
  __tablename__ = 'user'

  # 指定id映射到id字段; id字段为整型，为主键
  id = Column(Integer, primary_key=True)
  # 指定name映射到name字段; name字段为字符串类形，
  name = Column(String(20))
  fullname = Column(String(32))
  password = Column(String(32))
  password1 = Column(String(32))


  def __repr__(self):
    return "<User(name='%s', fullname='%s', password='%s')>" % (
      self.name, self.fullname, self.password)



