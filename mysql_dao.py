# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:28:00 2016

@author: shivani
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
DATABASEURI = "mysql+mysqlconnector://aheicklen:mass67@mysql.columbiasurf.dreamhosters.com:3306/columbiaamgen" 
engine = create_engine(DATABASEURI)

def createDatabaseConnection():
    try:
        conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        conn = None
    return conn
    
def createNewUser(conn,name,passwrd,userid):
    metadata = MetaData(conn)
    user_info = Table('userInfo', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==name)
    rs = s.execute()
    if rs.fetchone():
        return "Error"
    conn.execute('INSERT INTO userInfo VALUES (%s, %s, %s)', [name,passwrd,userid])
    
def getUser(conn,userid):
    metadata = MetaData(conn)
    user_info = Table('userInfo', metadata, autoload=True)
    s= user_info.select(user_info.c.Id==userid)
    rs = s.execute()
    a=rs.fetchone()
    u = User(rs["Username"],rs["Password"],rs["Id"],True)
    return u