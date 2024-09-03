import torchaudio
import torch
from ChatTTS import ChatTTS
import soundfile
from IPython.display import Audio
chat = ChatTTS.Chat()
chat.load_models(compile=False)
# 载入保存好的音色


class Tts():
    def __init__(self):
        pass

    # 语音模型
    def chat_sound(self, texts, infer_code):
        # refine_text = chat.infer(texts, refine_text_only=True)
        wavs = chat.infer(texts, params_infer_code=infer_code)
        return wavs

    # 输出与下载
    def tts_response(self, answer, infer_code):
        wavs = self.chat_sound(answer, infer_code)
        print("___"*10)
        torchaudio.save("output/output_d1.wav", torch.from_numpy(wavs[0]), 24000)
        return wavs