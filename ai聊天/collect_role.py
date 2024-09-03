import streamlit as st
import os
from dataclasses import dataclass, asdict
from sqlalchemy import insert
from sqlalchemy import Table, Column, Integer, String, DateTime, Text, MetaData, SmallInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

# 收集角色信息
@dataclass
class ChatSession:
    role: str
    role_name: str
    role_personality: str

class role_collect():
    def __init__(self):
        pass

    def role_prompt(self, role, role_name, role_personality):
        all_role = ChatSession(role, role_name, role_personality)
        print("角色信息：", role_name)
        self.store(all_role)


    def store(self,all_role: ChatSession):

        with SessionLocal.begin() as sess:
            q = insert(
                chat_session_table
            ).values(
                [asdict(all_role)]
            )
            sess.execute(q)


db_file = "chatbot.db"

if os.path.exists(db_file):
    os.remove(db_file)
engine = create_engine(f"sqlite:///{db_file}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata_obj = MetaData()
chat_session_table = Table(
    "chat_session_table",
    metadata_obj,
    Column("role", String(16)),
    Column("role_name", String(32)),
    Column("role_personality", String(32)),

)

metadata_obj.create_all(engine, checkfirst=True)
print("数据库创建成功！")