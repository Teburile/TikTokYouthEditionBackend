from databaseinit import Question
from databaseManager import register
from databaseManager import login
from databaseManager import DBSession
from databaseManager import questionShuffle
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.types import StrictBool
from starlette.responses import StreamingResponse
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import relation, sessionmaker

app=FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

def get_database():
    DATABASE_URL = "sqlite:///./Data.db"
    engine=create_engine(DATABASE_URL)
    DBSession=sessionmaker(bind=engine)
    database = DBSession()
    try:
        return database
    finally:
        database.close()


#login
class AccountLogin(BaseModel):
    id:int
    password:str
    role:str
    name:str


@app.post("/login")
async def _login(accountLogin:AccountLogin):
    return login(get_database(),accountLogin.id,accountLogin.password,accountLogin.role)


#register
class AccountTem(BaseModel):
    id:int
    password:str
    role:str
    name:str

@app.post("/register")
async def _register(accountTem:AccountTem):
    return register(get_database(),accountTem.id,accountTem.password,accountTem.role,accountTem.name)
    #return 'ok'

@app.get("/verify")
async def verificationQuestion():
    return questionShuffle(get_database())