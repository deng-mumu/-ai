import streamlit as st
from TTs_down import download_speaker
from decide import ManWoman

manwoman = ManWoman()
# 调用模型


def get_sql(inputs_text=""):
    # 默认为空
    if inputs_text == "":
        inputs = "no"
    else:
        inputs = inputs_text
    # 输入no时直接对信息
    if inputs == "no":
        from use_sql import query_chat_session
        query_chat = query_chat_session()
        print("no")
        return query_chat
    # 输入为yes时重新读信息
    elif inputs == "yes":
        from use_sql import query_chat_session
        query_chat = query_chat_session()
        print("yes")
        return query_chat
    else:
        st.error("输入错误，请重新输入")


def get_prompt():
    query_chat = get_sql()
    req = []
    for i in range(len(query_chat[0])):
        if i <= 2:
            inx = -1 * (i + 1)
            # print(query_chat[0][inx])
            req.append(query_chat[0][inx])
        else:
            break
    role = req[2]  # 男/女角色
    role_name = req[1]
    role_personality = req[0]
    prompt = f'''我与你的【任何对话】都必须严格执行以下角色要求。你叫{role_name}，
    我与你的对话必须严格遵守以下角色要求，你将扮演我的【{role}】，我的【{role}】必须严格遵守以下角色要求：
    姓名：{role_name}。性格：{role_personality}。
    记住你不是AI，请你完全沉浸在{role}的角色里，我们的任何对话都要用{role_name}的口吻回答我，
            回答不能超过50字，根据聊天话题延展你自己的想法。
            不能有解释类型的逻辑，表达要带有角色的性格特点。
    '''
    print("finish prompt")
    w_m = manwoman.similarity(role)
    print(w_m)
    info = download_speaker(w_m)
    return prompt, info
