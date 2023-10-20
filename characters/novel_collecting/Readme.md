

# ChatHaruhi的小说数据和ChatBot数据众筹计划

以下是Claude编写的广告词（我觉得还行）

## 加入ChatHaruhi - 让我们一起打造中文原创的开源角色扮演聊天机器人! :cn:

项目链接 [novel_collecting](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/novel_collecting)

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/who_is_next.jpg">
</p>

Character.AI等应用已经以其丰富多样的角色聊天体验吸引了超过千万级别月活用户。作为基于大语言模型角色扮演的开源中文实现版本,ChatHaruhi正在蓄势待发,准备发挥社区力量,提供更出色的本地化体验。

在这里,你可以选择热爱的小说和角色,利用我们提供的工具和指南,进行语料提取并将人物上传到Hugging Face。你的每一份贡献都将直接帮助ChatHaruhi拥有更多生动的游戏角色! :heart:

我们欢迎每一位热情的开发者加入,不管你是资深专家还是新手学习者。在这里,你可以通过技术为中文文学作品注入新生命,并参与构建一个具有影响力的开源项目。

加入我们,见证ChatHaruhi与众不同的崛起!这是一次难得的机遇,让我们共同打造中文原创角色的殿堂,提供更出色的本地化聊天体验。你的每个贡献都将推动它的成长! :muscle:


---

- [简介](#简介)
- [关于StoryTeller](#关于StoryTeller)
- [代码工具介绍](#代码工具介绍)
    - [小说中对话抽取工具](#小说中对话抽取工具)
    - [小说重写成jsonl的脚本介绍](#小说重写成jsonl的脚本介绍)
    - [特定角色的Chatbot提取](#特定角色的Chatbot提取)
    - [为角色总结合适的系统提示词](#为角色总结合适的系统提示词)
    - [抽取embedding之后上传到HuggingFace](#抽取embedding之后上传到HuggingFace)
    - [重新从ChatHaruhi中载入这个角色并与之聊天](#重新从ChatHaruhi中载入这个角色并与之聊天)
- [FAQ](#FAQ)
- [目前已经完成的数据](#目前已经完成的数据)
- [目前已经抽取的ChatBot](#目前已经抽取的ChatBot)

---


## 简介

以下是正经的文档叙述:

从8月开始，ChatHaruhi已经有一套完整的小说抽取——总结，形成Chatbot的流程

同时，我们也在准备开始制作新的StoryTeller，可以结合更多Chatbot来进行小说创作，或者说让几个Chatbot聚在一起进行聊天

目前，在8月底和9月初，我们对小说抽取和chatbot进行了重构，目前我们的系统有以下特点

- [x] 可以从一整本长篇的小说（最好是第三人称，最好多包含一些对话），抽取剧情梗概 和 角色对话，重写成结构化的一个jsonl文件
- [x] 可以选定特定的人物，总结这个角色chatbot所需的texts语料
- [x] 有特定的脚本可以指导你如何确定角色的prompt
- [x] 给定一个角色，将texts抽取embedding，结合用户设计的prompt，生成需要上传到hugging face的jsonl
- [x] 可以在ChatHaruhi2.0层面调用 到hugging去拖特定的人物，然后与之对话 

# 关于StoryTeller

storyteller是ChatHaruhi的一个后续分支项目，目前的作者有鲁叔，米唯实和冷子昂。我们希望形成一个整体的系统，不仅仅是能代表一个角色进行对话。而是能够给出整体的旁白、各个角色的对话选择和对话，甚至去续写更复杂的剧情和甚至给出图片等模态数据的穿插。

## 如何贡献数据
我之后会在github对应的页面写一个表格。你可以在抽取前先和我说一声，我就会记录在表格中。这样避免其他人重复抽取。然后你抽取之后把重组的jsonl给我就可以了。

chatbot的部分不需要提取，当然，反正小说都抽取了，可以顺便提取特定人物的chatbot，上传到hugging face，这个也和我说一声。我后面会做一个页面也统一登记大家抽取过的人物。这样ChatHaruhi能够使用的人物就越来越多了。

## 计算storyteller的作者

抽取两本以及以上（每本小说需要至少有200*1500个token的chunk）的作者会计算为storyteller的作者，如果我后面为storyteller续写工作的话。

如果你想成为chatharuhi后续arxiv更新版本的作者，需要贡献完整的chatbot数据，这个数量我回头再定一下，初步想至少给6个经典角色吧。
非代码作者排序就根据大致的数据供应量来排序吧

## 代码贡献

数据我都会公开出来，怎么参与到代码工作。我还没想清楚。当然你也可以拿数据自己训了玩。

代码我回头看看我和miweishi加起来够不够 不够的话会加人


# 抽取-整合-chatbot提取详细说明书

## Step 1 小说抽取

请使用这个文件[新小说抽取_release.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/新小说抽取_release.ipynb)

使用说明

1. 配置OpenAI Key

   ```python
   import os
   
   key = 'sk-VvF4' # edit here
   ```

2. 指定下载小说 wget后面的网址以及文件路径

   ```python
   !wget https://raw.githubusercontent.com/LC1332/Prophet-Andrew-Ng/main/langchain/%E5%B0%84%E9%9B%95%E8%8B%B1%E9%9B%84%E4%BC%A0.txt
   
   input_name = '/content/射雕英雄传.txt'
   ```

3. 指定保存位置

   ```python
   # mount google drive
   from google.colab import drive
   drive.mount('/content/drive')
   
   import os
   save_folder = "/content/drive/MyDrive/StoryGPT/shediaoyingxiongzhuan_extract"
   ```

4. 运行至notebook最后一个单元

   ```python
   import os
   import json
   from tqdm import tqdm
   
   # save_folder = "/content/drive/MyDrive/GPTData/weixiaobao_extract"
   
   for i in tqdm(range(len(chunk_text))):
      ...
   ```

## Step 2 抽取后重组

请使用这个文件[对话和摘要重组小说_两种方式.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/对话和摘要重组小说_两种方式.ipynb)

使用说明——使用抽取出原chunk做法

1. 必须配置保存路径以及抽取后路径

   ```python
   # 储存txt和jsonl的文件夹路径。如需修改，请与下方自动化循环保持一致
   
   save_folder_path =  "/content/drive/MyDrive/reorganized_story_shediaoyingxiongzhuan"
   
   # chunk所在文件夹，请以_raw结尾
   folder_path = f"/content/drive/MyDrive/shediaoyingxiongzhuan_extract"
   ```

2. 可选择性配置（一般来说不用改）

   ```python
   # 故事名字，默认为_raw之前的名字
   story_name_en = os.path.basename(folder_path).split("_")[0]
   
   # 测试ID
   id = 200
   
   # 默认的保存路径
   save_jsonl_path = f"/content/drive/MyDrive/reorganized_story_{story_name_en}/reorganized_{story_name_en}.jsonl"
   save_txt_path = f"/content/drive/MyDrive/reorganized_story_{story_name_en}/reorganized_{story_name_en}.txt"
   
   # 默认抽取出的dialogue和summary文件位置/如果有不同请在此处和底部自动程序中修改
   save_folder = f"/content/drive/MyDrive/{story_name_en}_extract"
   
   dialoge_file = os.path.join(save_folder, f"{id}_dialogue.txt")
   summarzie_file = os.path.join(save_folder, f"{id}_sum.txt")
   ```

3. 运行至保存代码部分

   ```markdown
   # 运行到此处，txt和jsonl文件已保存在/content/drive/MyDrive/reorganized_story_{story_name_en}下
   ```

如果重新从原小说抽取，请将

```python
# 如果你要想从content重新切分，请在开头运行以下代码

!wget https://raw.githubusercontent.com/LC1332/Prophet-Andrew-Ng/main/langchain/%E7%AC%91%E5%82%B2%E6%B1%9F%E6%B9%96.txt
```

切分代码首先运行，随后运行

```python
# 手动导入ID，继续向下运行以测试，最后根据ID循环
raw_text = chunk_text[ id ]

chunk_sum = []
unique_chunk_sum = []
```

抽取后匹配代码之后部分

## Step 3 小说chatbot抽取

请使用这个文件[多ChatBot抽取.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/多ChatBot抽取.ipynb)

使用说明

1. 配置一些参数

   ```python
   # 参数设置
   
   # 支持跨越多少行寻找目标角色，也即控制段内行间距不超过该值
   max_find_lines = 10
   
   max_token_num = 500
   #################################以上尽量不修改####################################
   # target_role支持 空字符串(默认前三个)或者List of string 如果出错默认保存第一个
   target_role = ['郭靖', "欧阳锋"]
   
   # 输入文件路径
   input_name = '/content/shediaoyingxiongzhuan.jsonl'
   
   # 保存路径
   savepath = '/content/texts'
   os.system(f"rm -rf {savepath}")
   os.makedirs(savepath, exist_ok=True)
   ```

2. 运行至notebook最后一个单元

   ```python
   for role_cur_name in role_extract :
     chat_ids, previous_scene_ids = output_scene_chat_id(data, role_cur_name)
     chat_ids_in_chunk, chat_id2previous_scene_id = divide_chats2chunks(chat_ids, previous_scene_ids)
     appended_key, final_chunks = id2texts(data, chat_ids_in_chunk, chat_id2previous_scene_id)
     save_chunk2zip(savepath+"/"+role_cur_name, role_cur_name, final_chunks) #如果你想修改保存的zip名称，请修改本函数的第二个参数save_title
   ```

3. 从保存/content/{role_cur_name}_text.zip中下载

   ```
   Zipped folder saved to /content/郭靖_text.zip
   Zipped folder saved to /content/欧阳锋_text.zip
   ```

## Step 4 根据GPT的建议编写人物的system_prompt


当然这个脚本其实没有openai的key直接复制prompt到claude也可以

[system_prompt_suggestion.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/system_prompt_suggestion.ipynb)


## Step 5 抽取embedding之后上传到HuggingFace

这个需要GPU，不然语料多了有点慢

[chatbot的embedding抽取和jsonl生成.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/chatbot%E7%9A%84embedding%E6%8A%BD%E5%8F%96%E5%92%8Cjsonl%E7%94%9F%E6%88%90.ipynb)

## Step 6 使用ChatHaruhi2.0载入

这个使用ChatHaruhi2.0

如果你是pip install的代码应该是这样

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_from_hf = 'chengli-thu/linghuchong', \
                      llm = 'openai')

response = chatbot.chat(role='小师妹', text = '冲哥。')
print(response)
```

如果你是github clone的，chatharuhi要换成大些ChatHaruhi

具体可以看这个脚本 [test_pull_role_form_hf.ipynb](https://github.com/LC1332/Haruhi-2-Dev/blob/main/notebook/test_pull_role_form_hf.ipynb)

# 代码工具介绍

## 小说中对话抽取工具

（需要openai key，尽量在colab或者外网ip运行）

抽取工具已经ready，由李鲁鲁实现完成

在  [新小说抽取.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/%E6%96%B0%E5%B0%8F%E8%AF%B4%E6%8A%BD%E5%8F%96_release.ipynb)

抽取dialogue有时候会产生一些噪音，另外kor的例子最好换成你的小说的例子

## 小说重写成jsonl的脚本介绍

这个工具由米唯实开发

[对话和摘要重组小说_两种方式.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/ChatBot%E6%8A%BD%E5%8F%96.ipynb)

现在能跑，mws还在进一步清理

## 特定角色的Chatbot提取

chatbot的提取工具已经有初步的版本，由李鲁鲁开发

[多ChatBot抽取.ipynb]([Chat-Haruhi-Suzumiya/characters/novel_collecting/多ChatBot抽取.ipynb at main · LC1332/Chat-Haruhi-Suzumiya (github.com)](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/多ChatBot抽取.ipynb))

## 为角色总结合适的系统提示词

（需要openai key，尽量在colab或者外网ip运行）

当然这个脚本其实没有openai的key直接复制prompt到claude也可以

[system_prompt_suggestion.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/system_prompt_suggestion.ipynb)

## 抽取embedding之后上传到HuggingFace

这个需要GPU，不然语料多了有点慢

[chatbot的embedding抽取和jsonl生成.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/chatbot%E7%9A%84embedding%E6%8A%BD%E5%8F%96%E5%92%8Cjsonl%E7%94%9F%E6%88%90.ipynb)

## 重新从ChatHaruhi中载入这个角色并与之聊天

[test_pull_role_form_hf.ipynb](https://github.com/LC1332/Haruhi-2-Dev/blob/main/notebook/test_pull_role_form_hf.ipynb)



# FAQ

### 为什么要把小说结构化重写

其实我们很容易找到千本以上的小说资源。但是一方面chatbot需要的文本格式是需要重新对小说抽取。另一方面，鲁叔认为把小说重整化之后，更容易用更少的训练数据就获得效果。如果我们有非常大的训练资源，我们可以放更多的小说一起训练。

### 多模态
多模态准备怎么搞吗？ 鲁叔这边暂时没有什么直接启动的计划，但是冷子昂在收集。你可以联系他

### Scene的数据是怎么来的
是GPT总结来的，然后scene和dialogue再根据原文把顺序align回去。

### 可以抽取英文小说吗？
可以的！欢迎！ 但是鲁叔自己不看英文小说，我可能抽一本哈利波特，一本冰与火 抽一本暮光之城就不搞了 哎呀感觉 指环王也值得抽
### 可以抽取其他语言的小说吗？
别，主要是本地模型的tokenizer不太支持。。
### 如果我愿意整理小说运行代码，但是没有openai key
如果确实能抽取，这边可以考虑赞助给你一些key，这个具体的我和运维同学去讨论一下。
### 会去支持其他的embedding吗
我看m3e模型比较小，考虑之后支持一下。我想找个同时支持中英文，模型不大，性能又还可以的embeding模型。
### 有微信群吗
懒得管理微信群，如果一定要有一个，我回头就用冷子昂拉的那个群吧。

# 目前已经完成的数据

| 小说 | kor抽取 | jsonl和txt | 备注|
|-|-|-|-|
| 笑傲江湖 | DONE | DONE | |
| 倚天屠龙记 | DONE,已发给mws | DONE mws | |
| 天龙八部 | DONE,已发给mws | DONE mws | |
| 射雕英雄传 | DONE,已发给mws | DONE mws | |
| 甄嬛传 | DONE 冷子昂 |  | |
| 庆余年 |  |  | |
| 凡人修仙传 | doing 李鲁鲁 |  | |
| 元龙 | DONE 李鲁鲁 |  | |
| 赘婿 |  |  |   |
| 无上杀神 |  |  | |
| 鬼吹灯(盗墓笔记) |  |  | mws来抽 |
| 魔道祖师(陈情令) |  |  | |
| 隐秘的角落 |  |  | |
| 斗罗大陆 | doing 冷子昂 |  | |
| 花千骨 |  |  | |
| 斯巴达300勇士(300) |  |  | |
| 绝代双骄 |  |  | |
| 情深深雨濛濛 |  |  | |
| 我师兄实在太稳健了 |  |  | |
| 一念永恒 |  |  | |

# 目前已经抽取的ChatBot

| 人物 | hf地址 | 来自小说 | 备注 |
| - | - | - | - |
| 令狐冲 | [chengli-thu/linghuchong](https://huggingface.co/datasets/chengli-thu/linghuchong) | 笑傲江湖 | |
| 岳不群 | [chengli-thu/yuebuqun](https://huggingface.co/datasets/chengli-thu/yuebuqun) | 笑傲江湖 | |
| 鸠摩智 | [hhhwmws/jiumozhi](https://huggingface.co/datasets/hhhwmws/jiumozhi) | 天龙八部 | |
| 萧峰 | [hhhwmws/xiaofeng](https://huggingface.co/datasets/hhhwmws/xiaofeng) | 天龙八部 | |
| 丁春秋 | [hhhwmws/dingchunqiu](https://huggingface.co/datasets/hhhwmws/dingchunqiu) | 天龙八部 | |
| 虚竹 | [hhhwmws/xuzhu](https://huggingface.co/datasets/hhhwmws/xuzhu) | 天龙八部 | |
| 谢逊 | [hhhwmws/xiexun](https://huggingface.co/datasets/hhhwmws/xiexun) | 倚天屠龙记 | |
| 张无忌 | [hhhwmws/zhangwuji](https://huggingface.co/datasets/hhhwmws/zhangwuji) | 倚天屠龙记 | |
| 赵敏 | [hhhwmws/zhaomin](https://huggingface.co/datasets/hhhwmws/zhaomin) | 倚天屠龙记 | |
| 周芷若 | [hhhwmws/zhouzhiruo](https://huggingface.co/datasets/hhhwmws/zhouzhiruo) | 倚天屠龙记 | |
| 黄药师 | [hhhwmws/huangyaoshi](https://huggingface.co/datasets/hhhwmws/huangyaoshi) | 射雕英雄传 | |
| 欧阳锋 | [hhhwmws/ouyangfeng](https://huggingface.co/datasets/hhhwmws/ouyangfeng) | 射雕英雄传 | |
| 黄蓉 | [hhhwmws/huangrong](https://huggingface.co/datasets/hhhwmws/huangrong) | 射雕英雄传 | |
| 郭靖 | [hhhwmws/guojing](https://huggingface.co/datasets/hhhwmws/guojing) | 射雕英雄传 | |
| 孙悟空 | [sibozhu/wukong](https://huggingface.co/datasets/sibozhu/wukong) | 西游记 | |