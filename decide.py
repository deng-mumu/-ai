from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv, find_dotenv
from sklearn.metrics.pairwise import cosine_similarity
_ = load_dotenv(find_dotenv())
client = ZhipuAI(api_key=os.getenv("API_KEY"))


class ManWoman:
    def __init__(self):
        pass

    def embedding_man(self, text):
        emb = client.embeddings.create(
            model="embedding-2",
            input=text,
        )
        return emb.data[0].embedding

    # 通过相似度来对比角色是男性还是女性
    def similarity(self, role):
        text = self.embedding_man(role)
        man = self.embedding_man("男性")
        woman = self.embedding_man("女性")
        if cosine_similarity([text], [man])[0][0] > cosine_similarity([text], [woman])[0][0]:
            return "男性"
        else:
            return "女性"


if __name__ == '__main__':
    WM = ManWoman()
    print(WM.similarity("汪星人"))
