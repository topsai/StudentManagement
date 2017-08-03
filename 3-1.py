import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("mysql+pymysql://root:123456@192.168.100.5/test?charset=utf8",
                       encoding='utf-8', echo=False)
Base = declarative_base()  # 生成orm基类


class UserFile(Base):
    __tablename__ = 'user_file'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    uaername = Column(String(32), unique=True, nullable=False)
    password = Column(String(32), nullable=False)


Base.metadata.create_all(engine)
