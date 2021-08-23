from sqlalchemy.sql.elements import False_
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.sqltypes import String
from databaseinit import Question, Teen, TimeRecord
from databaseinit import Parent
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import relation, sessionmaker
import random
import json

DATABASE_URL = "sqlite:///./Data.db"
engine=create_engine(DATABASE_URL)
DBSession=sessionmaker(bind=engine)

#register
def register(db:DBSession(),id:int,password:str,role:str,name:str):
    if role=="Parent":
        return parentRegister(db,id,password,name)
    else:
        return teenRegister(db,id,password,name)

def parentRegister(db:DBSession(),_id:int,_password:str,_name:str):
    tem=db.query(Parent).filter(Parent.id==_id).all()
    if(tem!=None):
        return {'status': 'failed'}
    else:
        new_parent=Parent(id=_id,password=_password,name=_name)
        db.add(new_parent)
        db.commit()
        return {'status': 'ok'}
        


def teenRegister(db:DBSession(),_id:int,_password:str,_name:str):
    tem=db.query(Teen).filter(Teen.id==_id).all()
    #print(tem)
    if(len(tem)>0):
        return {'status': 'failed'}
    else:
        new_teen=Teen(
            id=_id,
            password=_password,
            name=_name,
            uid=_name,
            flag=False,
            time=0,
            beingTime=0,
        )
        db.add(new_teen)
        db.commit()
        return {'status': 'ok'}


#login
def login(db:DBSession(),id:int,password:str,role:str):
    if role=="Parent":
        return parentLogin(db,id,password)
    else:
        return teenLogin(db,id,password)

def parentLogin(db:DBSession(),_id:int,_password:str):
    tem=db.query(Parent).filter(Parent.id==_id).all()
    if(len(tem)==0):
        return {'status': 'failed'}
    else:
        if(tem[0].password!=_password):
            return {'status': 'failed'}
        else:
            return {'status': 'ok'}

def teenLogin(db:DBSession(),_id:int,_password:str):
    tem=db.query(Teen).filter(Teen.id==_id).all()
    if(len(tem)==0):
        return {'status': 'failed'}
    else:
        if(tem[0].password!=_password):
            return {'status': 'failed'}
        else:
            return {'status': 'ok'}



#verify the right to upload video
def questionShuffle(db:DBSession()):
    listnum=[1,2,3,4,5]
    random.shuffle(listnum)
    basic_info={}
    verifyQuestions=[]    
    for order in listnum:
        tem=db.query(Question).filter(Question.id==order).all()
        questionJson=json.loads(json.dumps(basic_info))
        questionJson['question']=tem[0].description
        selection=[]
        selection.append(tem[0].selectionA)
        selection.append(tem[0].selectionB)
        selection.append(tem[0].selectionC)
        selection.append(tem[0].selectionD)
        questionJson['options']=selection
        questionJson['answer']=tem[0].ansthor
        verifyQuestions.append(questionJson)
    verify=json.loads(json.dumps(basic_info))
    verify['verifyQuestions']=verifyQuestions
    return verify


def setAbleToUpload(db:DBSession(),_id:int):
    tem=db.query(Teen).filter(Teen.id==_id).all()
    tem[0].flag=true
    return {"status": "ok"}


#userget
def userSelectRead(db:DBSession(),_id:int,_role:str):
    if _role=='Parent':
        return parentUserSelectRead(db,_id)
    else:
        return childUserSelectRead(db,_id)

def parentUserSelectRead(db:DBSession(),_id:int):
    basic_info={}
    mes=json.loads(json.dumps(basic_info))
    tem=db.query(Parent).filter(Parent.id==_id).all()
    mes['username']=tem[0].name
    if tem[0].child!=None:
        mes['alreadyBind']=True
        tem2=db.query(TimeRecord).filter(TimeRecord.child_id==tem[0].child.id).all()
        sum=0
        for i in tem2:
            sum+=i.watchTime
        mes['watchedTime']=sum
    else:
        mes['alreadyBind']=False
    return mes


def childUserSelectRead(db:DBSession(),_id:int):
    basic_info={}
    mes=json.loads(json.dumps(basic_info))
    tem=db.query(Teen).filter(Teen.id==_id).all()
    mes['uesrname']=tem[0].name
    mes['uniqueId']=tem[0].uid
    tem2=db.query(TimeRecord).filter(TimeRecord.child_id==tem[0].id).all()
    sum=0
    for i in tem2:
        sum+=i.watchTime
    mes['watchedTime']=sum
    return mes

#userpost
def bindTeen(db:DBSession(),_id:int,uniqueld:str):
    temParent=db.query(Parent).filter(Parent.id==_id).all()
    temChild=db.query(Teen).filter(Teen.uid==uniqueld).all()
    temChild.parent=temParent
    return {"status": "ok"}

def addWatchedRecord(db:DBSession(),_id:int,watchedTime:int):
    tem=db.query(Teen).filter(Teen.id==_id).all()
    new_record=TimeRecord(
        watchTime=watchedTime,
        date='22', #此处是日期
        child=tem[0]
    )
    db.add(new_record)
    db.commit()
    return {"status": "ok"}