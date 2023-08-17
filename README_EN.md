[SponsorShip](#SponsorShip) | [Report](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/report.md) | [Hiring](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Hiring.md) | [Personality](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

# Chat-Haruhi-Suzumiya

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()
[![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi)


<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/README.md">Chinese简体中文</a> |
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

This project is a work [in progress] (#TODO and Feature). With the release of the Arxiv version, we will publish a dataset supporting 32 characters and 52K dialogues, along with the corresponding local model and ChatHaruhi1.0 inference code, within a week. We will then begin refactoring the project for [ChatHaruhi2.0](#ChatHaruhi_2.0_Design).
 
This project is licensed under Apache 2.0, which permits commercial use. However, you still need to comply with other relevant agreements, including:

- The copyright of the character roles themselves.
  
- The terms of any APIs used in the project, such as OpenAI's agreement.
  
- The licenses of any models used in the project (for example, if we later adopt models from LlaMA or GLM, etc).

## Quick Start

To get started with the ChatHaruhi1.0 project, you can directly run the following Colab notebooks:

| Name |Colab Link| Description         |
|---|---|---|
| ChatHaruhi1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| Fully-featured client that allows switching between different character roles.                                                                                                 |

We are refactoring the code for ChatHaruhi 2.0, which will be solve the high module coupling problem of version 1.0 - it will be released as a pip-installable library with improved modularity.

## News

[2023-08-1X] ChatHaruhi Technical Report on arXiv.

[2023-06-07] Chat Haruhi Suzumiya won the second prize in the Create@AI Hackathon hosted by the Modelscope Community, co-sponsored by Alibaba Cloud and NVIDIA, and co-organized by Tianchi(top3), [video](https://www.bilibili.com/video/BV1Xh411A7kC/)

[2023-06-03] Honored with second prize(top3) and do oral presentation in July 17 for CAAI 8th-Big Data and Social Computing: 8th China National Conference, BDSC 2023, Urumqi, China, July 15–17, 2023 ，for more details [link](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

## Demo Video
 
The VITS model used in the video was generously provided by the [Haruhi Suzumiya Support Group](https://space.bilibili.com/201296348). We are still refining the perforamnce. Please note this [video](https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11) contains audio.

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
        <li><a href="#Current Results">Current Results</a></li>
        <li><a href="#Openness-Aware Personality Text Generation">Openness-Aware Personality Text Generation</a></li>
      </ul>
    </td>
  </tr>
</table>

## ChatHaruhi_2.0_Design
