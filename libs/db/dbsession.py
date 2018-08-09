#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 连接数据库的数据
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'tornado_01_OA'
USERNAME = 'tornado_user_01'
PASSWORD = 'tornado_user_01'
# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD,
                                                              HOSTNAME,
                                                              PORT,
                                                              DATABASE
                                                              )


# 1、创建一个engine引擎
engine = create_engine(DB_URI, echo=False )
# 2、sessionmaker生成一个session会话类
Session = sessionmaker(bind=engine)
# 3、创建一个session会话实例
dbSession = Session()
# 4、创建一个模型基类
Base = declarative_base(engine)



