

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


## 简介

以下是正经的文档叙述:

从8月开始，ChatHaruhi已经有一套完整的小说抽取——总结，形成Chatbot的流程

同时，我们也在准备开始制作新的StoryTeller，可以结合更多Chatbot来进行小说创作，或者说让几个Chatbot聚在一起进行聊天

目前，在8月底和9月初，我们对小说抽取和chatbot进行了重构，目前我们的系统有以下特点

- [x] 可以从一整本长篇的小说（最好是第三人称，最好多包含一些对话），抽取剧情梗概 和 角色对话，重写成结构化的一个jsonl文件
- [x] 可以选定特定的人物，总结这个角色chatbot所需的texts语料
- [x] 有特定的脚本可以指导你如何确定角色的prompt
- [ ] 给定一个角色，将texts抽取embedding，结合用户设计的prompt，生成需要上传到hugging face的jsonl
- [ ] 可以在ChatHaruhi2.0层面调用 到hugging去拖特定的人物，然后与之对话 

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

# 代码使用介绍

## 抽取工具的介绍

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

[characters/novel_collecting/ChatBot抽取.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/ChatBot%E6%8A%BD%E5%8F%96.ipynb)

## 为角色设计合适的system prompt

（需要openai key，尽量在colab或者外网ip运行）

当然这个脚本其实没有openai的key直接复制prompt到claude也可以

[system_prompt_suggestion.ipynb](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/characters/novel_collecting/system_prompt_suggestion.ipynb)

## 抽取embedding之后，上传到hugging face
我明天写一下这东西的代码

## 重新从ChatHaruhi2.0中载入这个角色，并与之聊天
我明天写一下这东西的代码

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