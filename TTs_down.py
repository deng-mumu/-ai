import torch


def download_speaker(text):
    if text == "男性":
        speaker = torch.load('speakers/b1hou.pth')
    elif text == "女性":
        speaker = torch.load('speakers/g1.pth')
    else:
        print("err")
    infer_code = {
        "spk_emb": speaker,
        # 'prompt': '[speed_10]',
        'temperature': 0.1,
        'top_P': 0.7,
        'top_K': 20,
        # "custom_voice": 3000,
        }
    print("finish download")
    return infer_code
