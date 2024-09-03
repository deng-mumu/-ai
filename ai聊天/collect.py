import os
from dotenv import load_dotenv, find_dotenv
from zhipuai import ZhipuAI
from dataclasses import dataclass, asdict
from typing import List
import uuid
import json
import re
from sqlalchemy import insert
from sqlalchemy import Table, Column, Integer, String, DateTime, Text, MetaData, SmallInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

_ = load_dotenv(find_dotenv())
client = ZhipuAI(api_key=os.getenv("API_KEY"))


def get_user_demand(msg):
    response = client.chat.completions.create(
        model="glm-4",
        messages=msg,
        temperature=0,
    )
    return response.choices[0].message.content

# 初始化部分数据类型
@dataclass
class User:
    user_id: str
    user_name: str

@dataclass
class ChatSession:
    user_id: str
    session_id: str
    role: str
    role_name: int
    role_personality: str


@dataclass
class ChatRecord:
    user_id: str
    session_id: str
    user_input: str
    bot_output: str


class UserDemand:
    def __init__(self):
        # 收集信息的prompt
        self.system_inp = """你现在是收集数据的助手，你的目的是收集角色，角色的姓名，角色的性格等信息：
        信息应该以JSON方式存储，包括三个key：role表示角色，role_name表示角色的姓名，role_personality表示角色的性格。

回复格式：
给用户的回复：{回复给用户的话}
获取到的信息：{"role": null, "role_name": null, "role_personality": null}
"""
        self.max_round = 10
        self.slot_labels = ["role", "role_name", "role_personality"]
        self.reg_msg = re.compile(r"\n+")
        self.ask_func = get_user_demand

    # 判断所需要的信息是否在字典中
    def check_over(self, slot_dict: dict):
        for label in self.slot_labels:
            if slot_dict.get(label) is None:
                return False
        return True

    def send_msg(self, msg: str):
        print(f"机器人：{msg}")

    def chat(self, user_id: str):
        # 随机id
        sess_id = uuid.uuid4().hex
        msg = [{"role": "user", "content": self.system_inp}]
        n_round = 0
        history = []
        slot = {"role": None, "role_name": None, "role_personality": None}
        while True:
            if n_round > self.max_round:
                bot_msg = "非常感谢您对我们的支持，再见。"
                self.send_msg(bot_msg)
                break

            try:
                bot_inp = self.ask_func(msg)
                print(bot_inp)
            except Exception as e:
                print(f"Error: {e}")
                bot_msg = "机器人出错，稍后将由人工与您联系，谢谢。"
                self.send_msg(bot_msg)
                break

            tmp = self.reg_msg.split(bot_inp)
            bot_msg = tmp[0].strip("给用户的回复：")
            self.send_msg(bot_msg)
            if len(tmp) > 1:
                slot_str = tmp[1].strip("获取到的信息：")
                slot = json.loads(slot_str)
                print(f"\tslot:{slot}")
            n_round += 1

            if self.check_over(slot):
                break

            user_inp = input()
            msg += [
                {"role": "assistant", "content": bot_inp},
                {"role": "user", "content": user_inp},
            ]

            record = ChatRecord(user_id, sess_id, bot_inp, user_inp)
            history.append(record)

        chat_sess = ChatSession(user_id, sess_id, **slot)
        self.store(history, chat_sess)

    # 将历史信息存入sql
    def store(self, history: List[ChatRecord], chat: ChatSession):
        with SessionLocal.begin() as sess:
            q = insert(
                chat_record_table
            ).values([asdict(v) for v in history])
            sess.execute(q)
        with SessionLocal.begin() as sess:
            q = insert(
                chat_session_table
            ).values(
                [asdict(chat)]
            )
            sess.execute(q)


db_file = "chatbot.db"

if os.path.exists(db_file):
    os.remove(db_file)

# 建立sql需要的信息
engine = create_engine(f"sqlite:///{db_file}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData()

chat_record_table = Table(
    "chat_record_table",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", String(64), index=True),
    Column("session_id", String(64), index=True),
    Column("user_input", Text),
    Column("bot_output", Text),
    Column("chat_time", DateTime),
)

chat_session_table = Table(
    "chat_session_table",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", String(64), index=True),
    Column("session_id", String(64), index=True),
    Column("role",  String(16)),
    Column("role_name", SmallInteger),
    Column("role_personality", String(32)),

)

metadata_obj.create_all(engine, checkfirst=True)

nick = "007"
user = User('007', nick)
chatbot = UserDemand()
chatbot.chat(user.user_id)


# 导出信息
def query_table(table: str):
    con = sqlite3.connect("chatbot.db")
    cur = con.cursor()
    q = cur.execute(f"SELECT * FROM {table}")
    return q.fetchall()


def query_chat_session():
    sql = query_table("chat_session_table")
    print("finish query chat session")
    return sql
