import requests
import inference_main

def set_model_path(path):
    inference_main.set_model_path(path)

def tts(text):
    res = requests.get(f"https://fanyi.baidu.com/gettts?lan=jp&text={text}&spd=5&source=web", headers={"Accept-Encoding": "gzip"})
    if res.status_code == 200:
        return res.content
    else:
        return None

def vit_haruhi(text, tran):
    voice = tts(text)
    if voice is None:
        print("TTS failed")
        return None
    return inference_main.infer_to("haruhi", tran, voice)


if __name__ == "__main__":
    set_model_path("vits_models/Haruhi_54000.pth")
    vit_haruhi("俺はモンキーキングでもベジータでもない", 8)
    vit_haruhi("私の青春は後悔していない", 8)
    vit_haruhi("不可能、絶対に不可能", 8)
    vit_haruhi("おはようございます", 8)