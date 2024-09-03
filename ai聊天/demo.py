from main import ChatGlm
from TTs import Tts
import streamlit as st
from get_prompt import get_sql

tts = Tts()

# # 创建一个标题和一个副标题
st.title("💬 Zhipu AI聊天（支持语音输出）")
st.text("是否需要重新生成prompt？yes/no\n")
if 'text' not in st.session_state:
    st.session_state['text'] = ''
inputs_text = st.text_input("请输入yes/no",key='text')
st.write("当前内容：", st.session_state['text'])

# 当输入yes时重新创建一次角色信息（每次启动只能重新创建一次目前没有解决这个问题）
if inputs_text == "yes":
    st.text("角色\n")
    role = st.text_input('请输入角色与你的关系')
    st.write('角色与你的关系', role)

    st.text("角色名称\n")
    role_name = st.text_input('请输入角色的姓名（例如：李华）')
    st.write('角色的姓名', role_name)

    st.text("角色性格\n")
    role_personality = st.text_input('角色的特色（例如：幽默，乐观）')
    st.write('角色性格', role_personality)

    # 创建一个按钮，当点击按钮时，将点击事件标记为已点击，利用按钮传输送角色信息
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click():
        st.session_state.clicked = True
        # 将点击事件标记为已点击
    st.button('完成输入', on_click=click)

    if st.session_state.clicked:
        if role and role_name and role_personality != "":
            from collect_role import role_collect
            role_collect().role_prompt(role, role_name, role_personality)
            get_sql(inputs_text)
            if "messages" not in st.session_state:
                st.session_state["messages"] = []
            del st.session_state["messages"]
            print("完成输入")
            st.session_state.clicked = False


chat_glm = ChatGlm()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state.messages.append({"role": "system", "content": chat_glm.prompt})

for i in st.session_state.messages[1:]:
    st.chat_message(i["role"]).write(i["content"])

if inpt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": inpt})
    # 将用户的输入添加到session_state中的messages列表中
    st.chat_message("user").write(inpt)
    # 在聊天界面上显示用户的输入
    ans = chat_glm.reponse(st.session_state.messages)
    print(ans)
    tts.tts_response(ans, chat_glm.info)
    # 将模型的输出添加到session_state中的messages列表中
    st.session_state.messages.append({"role": "assistant", "content": ans})
    # 在聊天界面上显示模型的输出
    st.chat_message("assistant").write(ans)
    # 保存语音
    audio_file = open('output/output_d1.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
    