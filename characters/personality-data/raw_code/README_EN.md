# A Big-Five Personality Study on ChatHaruhi: Assessing Personality Traits for Role-Playing Chatbots

This page contains two parts of content, personality testing for chatbots and generating text for specific openness. The former can test the personality traits of a role-playing chatbot.

## Quick Start

We will organize the code and publish it soon. We will prepare some quick code to support personality testing for a single ChatHaruhi bot.

## TODO

- [x] Publish report on arxiv
- [x] Put all experimental data and unorganized code on github 
- [ ] Publish sample code that can randomly select some questions from the question list to quickly test the personality of a chatbot

## Unorganized Code

| Code | Description |
|-|-|
| raw_code/心理问答设计.ipynb | Design first-person psychological questions |
| raw_code/心理问答审核.ipynb | Determine if each question can be used for personality testing | 
| raw_code/根据问题,获取chatbot的response回复.ipynb | Get response of each chatbot to each question |
| raw_code/分析角色每个dim的得分.ipynb | Get evaluation (text) of each personality dimension for each chatbot |
| raw_code/将评价转化为分数.ipynb | Convert text evaluation to scores |

## Unorganized Data

| Data | Description | 
|-|-|
| questions_verified.jsonl | Question list |
| raw_data/psy_test_gpt.txt | Responses of each chatbot to each question |
| raw_data/psy_eval_gpt_with_id.txt | Personality test results (text) for each bot |
| raw_data/psy_score_openai.txt | Converted scores from text |