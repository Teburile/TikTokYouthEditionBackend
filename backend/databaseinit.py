from datetime import datetime
from sqlalchemy import create_engine, engine
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from sqlalchemy.sql.expression import column, false, select, true
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, CHAR, DateTime, Integer, Time
from sqlalchemy.sql.type_api import TypeDecorator
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///./Data.db"
engine=create_engine(DATABASE_URL)
DBSession=sessionmaker(bind=engine)
Base=declarative_base()

class Teen(Base):
    __tablename__='teen'
    id=Column(Integer,primary_key=True)
    uid=Column(String)
    password=Column(String)
    flag=Column(Boolean)
    time=Column(Integer)
    beingTime=Column(Integer)
    name=Column(String)
    parent=relationship("Parent",back_populates="child")
    parent_id=Column(Integer,ForeignKey("parent.id"))
    timeRecord=relationship('TimeRecord',back_populates="child")

class Parent(Base):
    __tablename__='parent'
    password=Column(String)
    id=Column(Integer,primary_key=True)
    name=Column(String)
    #child_id=Column(Integer,ForeignKey("teen.id"))
    child=relationship('Teen',back_populates="parent")

class TimeRecord(Base):
    __tablename__='timeRecord'
    id=Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    child=relationship("Teen",back_populates="timeRecord")
    child_id=Column(Integer,ForeignKey("teen.id"))
    watchTime=Column(Integer)
    date=Column(DateTime,default=datetime.today())


#下面是添加问题
class Question(Base):
    __tablename__='question'
    id=Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    description=Column(String(300))
    selectionA=Column(String(300))
    selectionB=Column(String(300))
    selectionC=Column(String(300))
    selectionD=Column(String(300))
    ansthor=Column(Integer)

Base.metadata.create_all(bind=engine)

db=DBSession()

new_question1=Question(
    description="以下上传抖音青少年版的视频类型，不适合的是（ ）",
    selectionA="科普视频",
    selectionB="教学视频",
    selectionC="少儿动画视频",
    selectionD="美妆视频",
    ansthor=4,
)

db.add(new_question1)
db.commit()

new_question2=Question(
    description="以下行为对青少年来说，不值得提倡的是（ ）",
    selectionA="拾金不昧",
    selectionB="在家里帮助父母做一些力所能及的事",
    selectionC="随手乱扔垃圾",
    selectionD="劳逸结合，在学习后适度放松",
    ansthor=3,
)

db.add(new_question2)
db.commit()

new_question3=Question(
    description="进入青春期的青少年开始对父母的看法和结论产生怀疑，甚至反驳。这体现了青春期少年的（ ）",
    selectionA="独立性",
    selectionB="依赖性",
    selectionC="自制性",
    selectionD="冲动性",
    ansthor=4,
)

db.add(new_question3)
db.commit()

new_question4=Question(
    description="在与别人的沟通过程中，下列做法会起到反作用的是（ ）",
    selectionA="善于体谅",
    selectionB="强词夺理",
    selectionC="主动交流",
    selectionD="控制情绪",
    ansthor=2,
)

db.add(new_question4)
db.commit()

new_question5=Question(
    description="在实际生活中，人们在个人和集体的关系上有着不同的认识。以下说法更为准确的是（ ）",
    selectionA="一个人想要获得成功只需要自己的努力",
    selectionB="离开集体就不可能成功。人要获得成功必须处处依赖集体",
    selectionC="对集体有好处的事情就做，对个人有好处的不必做",
    selectionD="个人的成长离不开集体，集体力量的发挥需要每个人的共同努力",
    ansthor=4,
)


db.add(new_question5)
db.commit()
