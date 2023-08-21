[SponsorShip](#SponsorShip) | [Report](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/report.md) | [Hiring](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Hiring.md) | [Personality](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

<h1 id="BigTitle">
    Chat-Haruhi-Suzumiya
</h1>

# Reviving Anime Character in Reality via Large Language Model

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()
[![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi)

Temporary experience link: https://e6da3e2c0027ccf6a2.gradio.live

Temporary experience link2:  https://3a86a62a612c531114.gradio.live


<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/README.md">Chinese简体中文</a> |
        🤗 <a href="https://huggingface.co/spaces/silk-road/ChatHaruhi" target="_blank">Hugging Face</a>  |
        📜 <a href="https://arxiv.org/pdf/2308.09597.pdf" target="_blank">Paper</a>  |
        🗃️ <a href="https://huggingface.co/datasets/silk-road/Chat_Suzumiya_Fusion" target="_blank">54k Dataset</a>  |
    <p>
</h4>


**Chat-Haruhi-Suzumiya**is a language model that imitates the tone, personality and storylines of characters like Haruhi Suzumiya,


<details>
  <summary> The project was developed by Cheng Li, Ziang Leng, Chenxi Yan, Xiaoyang Feng, HaoSheng Wang, Junyi Shen, Hao Wang, Weishi Mi, Aria Fei, Song Yan, Linkang Zhan, Yaokai Jia, Pingyu Wu, and Haozhen Sun,etc. </summary>

This is an open source project and the members were recruited from open source communities like DataWhale.

Lulu Li( [Cheng Li@SenseTime](https://github.com/LC1332) )initiated the whole project and designed and implemented most of the features.
 
Ziang Leng( [Ziang Leng@SenseTime](https://blairleng.github.io) )designed and implemented the training, data generation and backend architecture for ChatHaruhi 1.0.

Chenxi Yan( [Chenxi Yan@Chengdu University of Information Technology](https://github.com/todochenxi) )implemented and maintained the backend for ChatHaruhi 1.0.

Junyi Shen( [Junyi Shen@Zhejiang University](https://github.com/J1shen) )implemented the training code and participated in generating the training dataset.

Hao Wang( [Hao Wang](https://github.com/wanghao07456) )collected script data for a TV series and participated in data augmentation.

Weishi Mi( [Weishi MI@Tsinghua University](https://github.com/hhhwmws0117) )participated in data augmentation.
 
Aria Fei( [Aria Fei@BJUT](https://ariafyy.github.io/) )implemented the ASR feature for the script tool and participated in the Openness-Aware Personality paper project.

Xiaoyang Feng( [Xiaoyang Feng@Nanjing Agricultural University](https://github.com/fengyunzaidushi) )integrated the script recognition tool and participated in the Openness-Aware Personality paper project.

Yue Leng ( [Song Yan](https://github.com/zealot52099) )Collected data from The Big Bang Theory. Implemented script format conversion.

scixing(HaoSheng Wang)( [HaoSheng Wang](https://github.com/ssccinng) ) implemented voiceprint recognition in the script tool and tts-vits speech synthesis.

Linkang Zhan( [JunityZhan@Case Western Reserve University](https://github.com/JunityZhan) ) collected Genshin Impact's system prompts and story data.

Yaokai Jia( [Yaokai Jia](https://github.com/KaiJiaBrother) )implemented the Vue frontend and practiced GPU extraction of Bert in a psychology project.

Pingyu Wu( [Pingyu Wu@Juncai Shuyun](https://github.com/wpydcr) )helped deploy the first version of the training code. 

Haozhen Sun( [Haozhen Sun@Tianjin University] )plot the character figures for ChatHaruhi. 



</details>

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/datasetOverview.png">
</p>

Chat-Haruhi-Suzumiya is one of the subproject of [Luotuo](https://github.com/LC1332/Luotuo-Chinese-LLM), which was initiated by Cheng Li, Ziang Leng, and Qiyuan Chen.
 
This project is a work [in progress](#todo-and-feature). With the release of the Arxiv version, we will publish a dataset supporting 32 characters and 52K dialogues, along with the corresponding local model and ChatHaruhi1.0 inference code, within a week. We will then begin refactoring the project for [ChatHaruhi2.0](#chatharuhi_20_design).
 
This project is licensed under Apache 2.0, which permits commercial use. However, you still need to comply with other relevant agreements, including:

- The copyright of the character roles themselves.
  
- The terms of any APIs used in the project, such as OpenAI's agreement.
  
- The licenses of any models used in the project (for example, if we later adopt models from LlaMA or GLM, etc).

## Quick Start

To get started with the ChatHaruhi1.0 project, you can directly run the following Colab notebooks:

| Name |Colab Link| Description         |
|---|---|---|
| ChatHaruhi1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| Fully-featured client that allows switching between different character roles. |
| ChatHaruhi2.0(EA) | <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/test_LangChainOpenAILLM.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | ChatHaruhi2.0 with OpenAI LLMs|

We are refactoring the code for ChatHaruhi 2.0, which will be solve the high module coupling problem of version 1.0 - it will be released as a pip-installable library with improved modularity.

## News

[2023-08-21] ChatHaruhi [tech report](https://arxiv.org/abs/2308.09597) on arXiv.

[2023-06-07] Chat Haruhi Suzumiya won the second prize in the Create@AI Hackathon hosted by the Modelscope Community, co-sponsored by Alibaba Cloud and NVIDIA, and co-organized by Tianchi(top3), [video](https://www.bilibili.com/video/BV1Xh411A7kC/)

[2023-06-03] Honored with second prize(top3) and do oral presentation in July 17 for CAAI 8th-Big Data and Social Computing: 8th China National Conference, BDSC 2023, Urumqi, China, July 15–17, 2023 ，for more details [link](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

## Demo Video
 
The VITS model used in the video was generously provided by the [Haruhi Suzumiya Support Group](https://space.bilibili.com/201296348). We are still refining the performance. Please note this [video](https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11) contains audio 📢 .

https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11

## Content

<table>
  <tr>
    <td>
      <p align="center">
        <img src="https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/figures/haruhi_suzumiya_bondage_rp.jpg" height="400">
      </p>
    </td>
    <td>
      <ul>
        <li><a href="#ChatHaruhi_2.0_Design">ChatHaruhi_2.0_Design </a></li>
        <li><a href="#Quick Start of each demo">Quick Start of Each Demo</a></li>
        <li><a href="#Demo Video">Demo Video</a></li>
        <li><a href="#Tutorial Video in Chinese">Tutorial Video in Chinese</a></li>
        <li><a href="#TODO and Feature">TODO and Feature</a></li>
        <li><a href="#Honors">Honors</a></li>
        <li><a href="#SponsorShip">SponsorShip </a></li>
        <li><a href="#Members">Members </a></li>
        <li><a href="#Citation">Citation</a></li>
      </ul>
    </td>
  </tr>
</table>

## ChatHaruhi_2.0_Design

ChatHaruhi started as an open source project with multimodal features like images and voice added to participate in competitions. Developers can now try the Gradio demo in the source code. However, this design isn't ideal for future research goals like adding characters, studying interactions, enhancing memory, or connecting to a Unity game backend.  
  
After this arxiv release, we will rebuild ChatHaruhi with the following planned interfaces:

```python
from ChatHaruhi import ChatHaruhi

chatbot = ChatHaruhi( system_prompt = 'prompt.txt', \
                      story_db = 'story_chroma_folder', \
                      llm = 'openai' )
                      
response = chatbot.chat(text = 'Can you introduce youself?', role = 'Kyon' )
```

The system will use a simple system_prompt parameter and vector database for access. It will support switching between LLMs like the locally trained model from this paper, Claude, Spark API, etc. For conversations using the ChatHaruhi-52K characters, you can use them directly out of the box below.
```python
from ChatHaruhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'Haruhi', \
                      llm = 'openai' )
                      
response = chatbot.chat(text = 'Can you introduce youself?', role = 'Kyon' )
```


For more things: https://github.com/LC1332/Haruhi-2-Dev 


## Quick Start of Each Demo



| Name |Colab Link| Description         |
|---|---|---|
| ChatHaruhi 1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| A functionally integrated client capable of supporting role switching                                                                                                 |
| Genesis                                                     |<a href="https://colab.research.google.com/github/LC1332/Prophet-Andrew-Ng/blob/main/prophet-code/haruhiLangChain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| the first gradio chat developed by Lulu Li |
| Baidu Studio Version                                               | [Baidu Studio Version](https://aistudio.baidu.com/aistudio/projectdetail/6386896) | A simplified version of Baidu Studio developed by DataWhale teaching assistant - Qijun Ma |
| HuggingFace Version                                            | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi) | HuggingFace Version                                                                                    |
| personality - College entrance exam essay | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/College_essays_gradio.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | College entrance exam essay generator tailored to high or low openness personalities，[link](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data) |
| personality-Chatbot                                               | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/PersonalityChatbot.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | Chatbot corresponding to high/low open personality，[link](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)  |
| Chat Megumi                                                 |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/gradio_megumi.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| Chat Megumi was created using a corpus collected by community friends. |

## Tutorial Video in Chinese

| Video | Description |
|---|---|
| [Roadmap in 5 minutes](https://www.bilibili.com/video/BV1Xh411A7kC/)    | AI Hackathon of Modelscope in Bilibi       |
| [DataWhale Presentation](https://www.bilibili.com/video/BV1ho4y1P75H) | Instructional video created for a DataWhale assignment |
| [Script Tool Tutorial](https://www.bilibili.com/video/BV1V8411S7eT)      |Step-by-step guide to using the yuki_builder scripting tool|
| [Character Data Format Tutorial](https://www.bilibili.com/video/BV1nu411H7Sy/)    |Tutorial on the character data format and converting text files to configuration files. |
| [ModelScope Tutorial in 40 minutes](https://www.bilibili.com/video/BV1Wm4y1W7XH) | 40-tutorial in entry-level, with an additional 40 minutes for discussion and Q&A |

  

## TODO and Feature

TODO:

- [x] train the model of the original corpus of 22k stories
- [x] release technical report on arxiv 
- [ ] release local inference code
- [ ] release trained model with 52k data
- [ ] Support local model and OpenAI's ChatHaruhi2.0, update to github
- [ ] quick install with **pip**


## Honors

- 🏆 Chat Haruhi Suzumiya won the second prize in the Create@AI Hackathon hosted by the Modelscope Community, co-sponsored by Alibaba Cloud and NVIDIA, and co-organized by Tianchi(top3) [video](https://www.bilibili.com/video/BV1Xh411A7kC/)

- 🏆 Honored with the second prize (top3) and do oral presentation in July 17 for CAAI 8th-Big Data and Social Computing: 8th China National Conference, BDSC 2023, Urumqi, China, July 15–17, 2023 [for more details](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

## SponsorShip

Due to Chat Haruhi Suzumiya adopts a strategy similar to CoT, which is 10-20 times more expensive than usual. Currently, API tokens are supported by community donations.

In addition, we are actively looking for GPUs (A100, A800). If you are willing to donate, please contact us. We greatly appreciate any support to help keep Chat Haruhi Suzumiya running.

If you are interested in sponsoring the [Luotuo Project](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships), please click on the [major project](https://github.com/LC1332/Luotuo-Chinese-LLM) or view the [sponsorship form](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md).

>[Back to top](#BigTitle)


## Members

- [Cheng Li@SenseTime](https://github.com/LC1332)  purposed the entire project and designed and implemented most of the functionality.

- [Ziang Leng@SenseTime](https://blairleng.github.io) designed and implemented the overall training, data generation and backend architecture of ChatHaruhi1.0.

- [Chenxi Yan@Chengdu University of Information Technology](https://github.com/todochenxi) implemented and maintained the backend of ChatHaruhi1.0 version.

- [Junyi Shen@Zhejiang University](https://github.com/J1shen) implemented the training code and participated in the generation of training dataset.

- [Hao Wang](https://github.com/wanghao07456) collected script data from My Own Swordsman and participated in the generation of augmented data.

- [Weishi MI@Tsinghua University](https://github.com/hhhwmws0117) participated in the generation of augmented data.

- [Aria Fei@BJUT](https://ariafyy.github.io/) implemented the ASR function of the script tool and participated in the Openness-Aware Personality paper sub-project.

- [Xiaoyang Feng@Nanjing Agricultural University](https://github.com/fengyunzaidushi) integrated the functions of the script recognition tool and participated in the Openness-Aware Personality paper sub-project.

- [Song Yan](https://github.com/zealot52099) collected data from The Big Bang Theory. Implemented script format conversion functionality.

- [HaoSheng Wang](https://github.com/ssccinng) implemented voiceprint recognition function in script tool, and tts-vits speech synthesis function.

- [Linkang Zhan@Case Western Reserve University](https://github.com/JunityZhan) collected system prompt and story data from Genshin Impact.

- [Yaokai Jia](https://github.com/KaiJiaBrother) implemented the Vue version of the frontend, and practiced GPU extraction of Bert in the psychology project.

- [Pingyu Wu@Juncai Shuyun](https://github.com/wpydcr) helped deploy the first version of the training code.

- [Haozhen Sun@Tianjin University](https://github.com/jcandzero) drew the mosaic of ChatHaruhi characters.


### Citation

Please cite the repo if you use the data or code in this repo.
```
@misc{li2023chatharuhi,
      title={ChatHaruhi: Reviving Anime Character in Reality via Large Language Model}, 
      author={Cheng Li and Ziang Leng and Chenxi Yan and Junyi Shen and Hao Wang and Weishi MI and Yaying Fei and Xiaoyang Feng and Song Yan and HaoSheng Wang and Linkang Zhan and Yaokai Jia and Pingyu Wu and Haozhen Sun},
      year={2023},
      eprint={2308.09597},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
[![Star History Chart](https://api.star-history.com/svg?repos=LC1332/Chat-Haruhi-Suzumiya&type=Date)](https://star-history.com/#LC1332/Chat-Haruhi-Suzumiya&Date)
---
If you have any suggestions for the project, such as the interface design of **ChatHaruhi2.0**,
or want to add references to the future version of this report, please submit the [issue](https://github.com/LC1332/Chat-Haruhi-Suzumiya/issues).
