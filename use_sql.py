# 将collect收集的信息导出
import sqlite3


def query_table(table: str):
    con = sqlite3.connect("chatbot.db")
    cur = con.cursor()
    q = cur.execute(f"SELECT * FROM {table}")
    return q.fetchall()


def query_chat_session():
    sql = query_table("chat_session_table")
    print("finish query chat session")
    return sql


if __name__ == ' __main__':
    
    sql = query_chat_session()
