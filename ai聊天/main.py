import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from zhipuai import ZhipuAI
from get_prompt import get_prompt
from TTs import Tts
from decide import ManWoman
# 调用模型
tts = Tts()
manwoman = ManWoman()

_ = load_dotenv(find_dotenv())
client = ZhipuAI(api_key=os.getenv("API_KEY"))


class ChatGlm():
    def __init__(self):

        self.prompt, self.info = get_prompt()
        self.msg = [{"role": "user", "content": self.prompt}]

    def reponse(self, msg):
        response = client.chat.completions.create(
            model="glm-4",
            messages=msg,
            temperature=0.7,
        )
        return response.choices[0].message.content

    def check_over(self, inpt):
        if "再见" in inpt or "拜拜" in inpt or "结束" in inpt:
            return True

    def chat(self, ):
        while True:
            outp = self.reponse(self.msg)
            inpt = input()
            self.msg += [
                {"role": "assistant", "content": outp},
                {"role": "user", "content": inpt},
            ]
            answer = self.reponse(self.msg)
            if self.check_over(inpt):
                break
            print(answer)



    # st.audio(wavs[0])
#
# if __name__ == '__main__':
#     ChatGlm().chat()