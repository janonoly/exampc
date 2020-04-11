from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#sqlite创建数据库连接
engine = create_engine('sqlite:///resources/exam.db?check_same_thread=False',encoding='utf-8', echo=True)
# engine = create_engine('sqlite:///../resources/exam.db?check_same_thread=False',encoding='utf-8', echo=True)
#先建立基本映射类，后边真正的映射类都要继承它
Base = declarative_base()

#导入models创建数据库表，只增加不会减少
from model import question,user
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
