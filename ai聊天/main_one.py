import os
from dotenv import load_dotenv, find_dotenv
from zhipuai import ZhipuAI
from TTs import Tts
from decide import ManWoman

_ = load_dotenv(find_dotenv())
client = ZhipuAI(api_key=os.getenv("ZhipuAI_API_KEY"))
# 判断是否需要重新生成角色进行对话
inputs = input("是否需要重新生成prompt？yes/no\n")
manwoman = ManWoman()
tts = Tts()
if inputs == "no":
    from use_sql import query_chat_session
elif inputs == "yes":
    from collect import query_chat_session


# 将角色的信息生成prompt
def get_prompt():
    query_chat = query_chat_session()
    req = []
    for i in range(len(query_chat[0])):
        if i <= 2:
            inx = -1 * (i + 1)
            # print(query_chat[0][inx])
            req.append(query_chat[0][inx])
        else:
            break
    role = req[2]
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
    # 根据角色信息进行判断要下载什么样的音色
    w_m = manwoman.similarity(role)
    tts.download_speaker(w_m)
    return prompt, role_name


class ChatGlm:
    def __init__(self):

        self.prompt, self.role_name = get_prompt()

    # 调用api
    def reponse(self, msg):
        response = client.chat.completions.create(
            model="glm-4",
            messages=msg,
            temperature=0.7,
        )
        return response.choices[0].message.content

    # 检测输入的是否是结束语
    def check_over(self, inp):
        if "再见" in inp or "拜拜" in inp or "结束" in inp:
            return True

    # 循环对话
    def chat(self):
        while True:
            # ai的要求
            msg = [{"role": "user", "content": self.prompt}]
            outp = self.reponse(msg)
            inp = input()
            # 记录上下文
            msg += [
                {"role": "assistant", "content": outp},
                {"role": "user", "content": inp},
            ]
            answer = self.reponse(msg)
            print(f"{self.role_name}:{answer}")
            tts.tts_response(answer)
            if self.check_over(inp):
                break


answer = ChatGlm().chat()