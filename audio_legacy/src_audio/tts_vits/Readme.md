## 凉宫春日的vits变声

### 安装环境

```
pip install -r requirements.txt
```

## 模型下载

[模型](https://huggingface.co/scixing/Haruhi_Vits/blob/main/Haruhi_54000.pth)该模型在程序中使用set_model_path加载

[hubert模型](https://huggingface.co/scixing/Haruhi_Vits/blob/main/hubert-soft-0d54a1f4.pt)该模型放入`tts_vits\hubert`文件夹下

## 使用方法

```python
# 设置模型路径
set_model_path("vits_models/Haruhi_54000.pth")
# 生成语音 第一个参数为文本 第二个参数为音高
vits_haruhi("真実はいつもひとつ", 8)
```