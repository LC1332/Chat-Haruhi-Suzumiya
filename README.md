中文 | English | 日本語

# Chat凉宫春日 Chat-Haruhi-Suzumiya

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()

Chat凉宫春日 是 模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，

<details>
  <summary> 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋等开发。 </summary>

李鲁鲁发起了项目，并完成了最早的版本，在多个微信群实现了测试。

冷子昂参与了早期Gradio的开发，并且参与了后端和前端的选型

闫晨曦将李鲁鲁的notebook重构为app.py

封小洋进行了中文转日文模型的选型

</details>

<table>
  <tr>
    <td>
      <p align="center">
        <img src="https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/figures/haruhi_suzumiya_bondage_rp.jpg" height="400">
      </p>
    </td>
    <td>
      <ul>
        <li><a href="#快速开始">快速开始</a></li>
        <li><a href="#快速开始">计划Feature</a></li>
        <li><a href="#赞助">赞助 | SponsorShip </a></li>
        <li><a href="#赞助">人员 </a></li>
        <li><a href="#TODO">TODO</a></li>
      </ul>
    </td>
  </tr>
</table>

本项目的核心思想是在prompt构造的时候利用[Luotuo-BERT](https://github.com/LC1332/Luotuo-Text-Embedding)，对经典剧情进行了搜索，作为Fewshot（或者说更接近CoT）的构造标准。

Chat凉宫春日是[Luotuo(骆驼)](https://github.com/LC1332/Luotuo-Chinese-LLM)的子项目之一, 后者由李鲁鲁, 冷子昂, 陈启源发起。

本项目采用Apache 2.0协议，也就是你可以利用项目中的代码进行商用。但是你仍然需要遵守包括 1.角色本身的版权方的协议 2.项目中使用的接口方，比如OpenAI的协议， 3.项目中使用的模型的协议（比如如果我们后期采用了LlaMA或者GLM的模型。）

本项目是DataWhale的5月学习的作业，其中闫晨曦，封小洋等同学都由DataWhale社区招募。

## 快速开始

|名称|colab链接|说明|
|---|---|---|
|万恶之源|<a href="https://colab.research.google.com/github/LC1332/Prophet-Andrew-Ng/blob/main/prophet-code/haruhiLangChain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 李鲁鲁最早开发的gradio Chat凉宫春日 |

## 计划Feature

我们计划最终产生一个多个前端版本的 Chat凉宫春日，具体特征如下

- Gradio版本

    - 可以在colab启动，方便任何人使用

    - 支持静态图的显示，念白经典台词的时候会同时显示对应的经典画面

    - (opt) 如果Gradio支持语音的话，再做一个合成日文语音的版本

- 本地版本

    - 支持一个Live2D的老婆，口型与语音同步

    - 支持输出的文本转成日文再用合成语音念出来

    - 争取换成haruhi酱的形象

- 后端特征

    - 理论上支持角色更换

    - 日语翻译支持本地/gpt3.5 模型的选择，能不花钱就不花钱呗

    - (后期) 支持使用本地模型去替换gpt3.5，能不花钱就不花钱

- (opt)研究部分

    - 研究聊天空间覆盖程度，看看GPT是否能生成更多的聊天

    - 不论用什么方式，把对话数据补充到接近5万条

    - 争取训练自己的Haruhi模型

    - 构思合理的定量化User Study

    - 争取写一个TechReport挂到arxiv


## 赞助

因为Chat凉宫春日采用了类似CoT的策略，相比于通常聊天，要贵上10-20倍，目前API token都采用社区捐赠的费用来支持。

另外我们在积极寻找服务器资源(A100，A800)，如果您愿意捐助，欢迎联系我们。

如果你有兴趣赞助Chat凉宫春日 或者 骆驼项目，请点击[主项目](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships)或者查看[赞助表单](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md)

If you are interested in sponsoring the [Luotuo Project](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships), please click on the [major project](https://github.com/LC1332/Luotuo-Chinese-LLM) or view the [sponsorship form](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md).

[回到开头](#BigTitle)


## TODO

持续招人中

https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/Hiring.md

---

基础的python后端

- [x] 将Notebook移动到一个app.py的文件中 (doing by 闫晨曦)
- [x] 确认app.py能够修改台词记录folder 这样可以存到本地或者colab启动的时候可以存到google drive
- [x] system prompt存成txt( characters/haruhi/system_prompt.txt )，支持切换。
- [x] 确认app.py能够正确调用haruhi的system prompt
- [ ] 冷子昂测试app.py
- [ ] 确认app.py能够启动gradio
- [x] app.py 支持设定max_len_story 和max_len_history 默认为 1500, 1200
- [ ] (opt) 前面都完成之后，项目可以转成public，方便从colab去拉取代码，建立一个colab脚本, 直接clone项目，调用app.py进行玩耍

闫晨曦 is working on that


---

新的后端任务

- [ ] 将text的embedding和字典做预存

我已经在characters/haruhi/images 上传了文件

同时text_image_dict里面存储了文件名和台词之间的关系

- [ ] 待鲁叔初步的图-文数据之后，做一个类，

支持文本embedding抽取、预存、载入、给定文本出(图片、相似度)

- [ ] 如果手快的话，再把这个出图片的整合到gradio里面去(新建一个后端任务)

---

带socket（或者其他本地与前端链接方式的后端）

这里前端可以去用https://github.com/Voine/ChatWaifu_Mobile  也可以去用别的

- [ ] 调研ChatWaifu的后端怎么和前端连接
- [ ] 制作一个foo的后端，看看能不能接入
- [ ] 待app.py有个基础版本后，修改为适合ChatWaifu的后端

贾曜恺 is working on that


---

中文到日文的训练

在hugging找一下有没有已经能用的中转日翻译 比如 ssmisya/zh-jp_translator K024/mt5-zh-ja-en-trimmed larryvrh/mt5-translation-ja_zh 

日文数据 https://huggingface.co/datasets?language=language:zh,language:ja&sort=downloads

- [x] 检查这个模型是不是直接能用(可以问鲁叔，要一些台词文件)
- [x] 如果模型很能用，任务就结束了，可以考虑训别的东西（一般不会）

（暂时选定这个模型）

- [ ] 搜集台词数据、搜集hugging face上所有能用的日文翻译数据
- [ ] 数据最好达到200k级别
- [ ] 问鲁叔要一下沈junyi之前的训练代码
- [ ] 训练中文转日文模型
- [ ] 对接测试

封小洋 is working on that

---

批量台词抽取

- [x] 等待鲁叔share数据

**注意：大量的图文、视频数据不要上传到git**
**放少量的测试数据是可以的**

- [ ] 实现台词和视频的对齐
- [ ] 实现视觉分类器，能够把Haruhi的台词部分抽取出来
- [ ] 鲁叔会整理一个jsonl文件，把haruhi在之前测试时候输出的话总结一下
- [ ] 然后我们根据ChatHaruhi输出的台词去retrive Haruhi剧中的台词，争取找一些高频出现的台词
- [ ] 图片保存为高度为480的jpg，这样小一点，容易存
- [ ] 我们只保留高频台词和对应的台本，形成text-image数据集，作为补充包 **这个大的数据不要上传到github**


---

李鲁鲁的self driving


- [x] 构建项目页
- [x] 招人
- [ ] 整理田野测试时候ChatHaruhi输出的台词
- [x] 去下载Haruhi的动画片视频，想办法先搞几张台词和图片的匹配
- [ ] 一个增强的gradio系统，支持根据台词显示haruhi的图片
- [x] 去二次元社区找更熟悉凉宫春日的同学众测
