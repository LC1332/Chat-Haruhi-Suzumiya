 English| [中文](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/research/personality/README.md) |[💡Paper](https://arxiv.org/abs/2310.17976)


# Does Role-Playing Chatbots Capture the Character Personalities? Assessing Personality Traits for Role-Playing Chatbots

### Setup

Ensure you have correctly installed `ChatHaruhi2` and all necessary dependencies. If not yet installed, you can do so with the following commands:

```bash
pip install torch torchvision torchaudio
pip install transformers openai tiktoken langchain chromadb zhipuai chatharuhi datasets jsonlines
```

Enter the code folder.
```bash
cd code
```

Set your openai apikey in config.json .

### Personality Assessment

To assess the personality of a specific ChatHaruhi Bot, use the following commands:

Quick Test:

```bash
python assess_personality.py --questionnaire_type mbti --character hutao --eval_setting sample
```

Balanced Effectiveness and Efficiency:

```bash
python assess_personality.py --questionnaire_type mbti --character hutao --eval_setting collective
```

Optimal Effectiveness:

```bash
python assess_personality.py --questionnaire_type mbti --character hutao --eval_setting batch --evaluator gpt-4 
```

Using the `sample` setting, the system will sample 20 questions from the questionnaire for testing. This process takes approximately 1-2 minutes. A full MBTI/Big Five test will take around 8-15 minutes, depending on whether batch evaluation is used.

### Parameter Explanation

#### `--questionnaire_type`
- Description: The type of questionnaire used for the personality test.
- Options: `bigfive`, `mbti`
- Default: `mbti`

#### `--character`
- Description: Character name, which can be in Chinese or English as listed in NAME_DICT.
- Default: `haruhi`

#### `--agent_llm`
- Description: The underlying LLM of ChatHaruhi. Here, `openai` is equivalent to `gpt-3.5-turbo`.
- Options: `gpt-3.5-turbo`, `openai`, `GLMPro`, `ChatGLM2GPT`
- Default: `gpt-3.5-turbo`

#### `--evaluator`
- Description: The method used to analyze questionnaire results for personality assessment. This can be an LLM like GPT or the 16Personality API (MBTI only).
- Options: `api`, `gpt-3.5-turbo`, `gpt-4`
- Default: `gpt-3.5-turbo`

#### `--eval_setting`
- Description: Evaluation setting. `batch` groups question-answer pairs and scores them multiple times using the LLM, `collective` evaluates based on all question-answer pairs for a specific dimension at once, `sample` starts by only sampling 20 questions from the questionnaire for the personality test.
- Options: `batch`, `collective`, `sample`
- Default: `batch`

#### `--language`
- Description: Language setting, currently only supports Chinese (cn).
- Options: `cn`, `en`
- Default: `cn`

## TODO

- [x] Publish report on arxiv
- [x] Put all experimental data and unorganized code on github 
- [x] Publish sample code that can randomly select some questions from the question list to quickly test the personality of a chatbot
- [x] Release a code that can conduct personality tests on a specific chatbot, covering the main experiments discussed in the article.

## Unorganized Code

Big Five

| Code | Description |
|-|-|
| raw_code/心理问答设计.ipynb | Design first-person psychological questions |
| raw_code/心理问答审核.ipynb | Determine if each question can be used for personality testing | 
| raw_code/根据问题,获取chatbot的response回复.ipynb | Get response of each chatbot to each question |
| raw_code/分析角色每个dim的得分.ipynb | Get evaluation (text) of each personality dimension for each chatbot |
| raw_code/将评价转化为分数.ipynb | Convert text evaluation to scores |

MBTI 
| Code                                   | Description                                   |
| ---                                    | ---                                           |
| raw_code/get_mbti_results.py            | Obtain chatbot's answers to MBTI questionnaire |
| raw_code/eval_mbti_closed.py            | Assess MBTI based on 16 Personality    |
| raw_code/eval_mbti_open.py              | Assess MBTI  based on LLM Evaluator, w/o grouping |
| raw_code/eval_mbti_multigroup.py        | Assess MBTI  based on LLM Evaluator, w/ grouping |


## Unorganized Data

Big Five 

| Data | Description | 
|-|-|
| questions_verified.jsonl | Question list |
| raw_data/psy_test_gpt.txt | Responses of each chatbot to each question |
| raw_data/psy_eval_gpt_with_id.txt | Personality test results (text) for each bot |
| raw_data/psy_score_openai.txt | Converted scores from text |

MBTI

MBTI-related
| Data                                                      | Description                                               |
| ---                                                       | ---                                                       |
| mbti_questions.jsonl                                      | Question list                                             |
| raw_data/mbti_labels.jsonl                                | MBTI personality labels for each bot                      |
| raw_data/mbti_results.jsonl                               | Answers to the MBTI questionnaire for each bot, includes open response and closed options |
| raw_data/mbti_results_closed.jsonl                        | MBTI test results based on 16 Personality                |
| raw_data/mbti_results_open.jsonl                          | MBTI test results based on LLM Evaluator (GPT-4), no grouping |
| raw_data/mbti_results_open_multigroup_split=True_gpt-4.jsonl | MBTI test results based on LLM Evaluator, with grouping  |

---

# Does Role-Playing Chatbots Capture the Character Personalities? Assessing Personality Traits for Role-Playing Chatbots 


<details>
  <summary> This project was developed by Wang Xintao, Tu Quan, Aria Fei, Leng Zi'ang, Li Lulu, and others. </summary>
This project is an open-source project.

Wang Xintao( [Xintao Wang@Fudan University](https://neph0s.github.io/) )was responsible for the MBTI personality tests, most of the chart statistics presented in this document, and the final organization of the LaTeX document.

Tu Quan( [Quan Tu@GSAI, Renmin University of China](https://github.com/morecry) )conducted the Big Five personality tests for other (non-OpenAI) language models and contributed to some of the images in the article.

Aria Fei( [Yaying Fei@Beijing University of Technology](https://ariafyy.github.io/) ) conducted the baseline personality tests for OpenAI and GLM.

Leng Zi'ang ( [Ziang Leng@Boston University](https://blairleng.github.io) )developed the program to convert textual evaluations into scores.

Li Lulu( [Cheng Li@SenseTime](https://github.com/LC1332) )proposed this project and was responsible for the design and coding of the Big Five personality test and evaluation prompts.

</details>

# Abstract

The emergence of large-scale pretrained language models has revolutionized the capabilities of new AI application, especially in the realm of crafting chatbots with distinct personas. 
Given the "stimulus-response" nature of chatbots, this paper unveils an innovative open-ended interview-style approach for personality assessment on role-playing chatbots, which offers a richer comprehension of their intrinsic personalities. 
we conduct personality assessments on 32 role-playing chatbots created by the ChatHaruhi library, across both the Big Five and MBTI dimensions, and measure their alignment with human perception. 
Evaluation results underscore that modern role-playing chatbots based on LLMs can effectively portray personality traits of corresponding characters, with an alignment rate of 82.8\% compared with human-perceived personalities. 
Besides, we also suggest potential strategies for shaping chatbots' personalities.
Hence, this paper serves as a cornerstone study for role-playing chatbots that intersects computational linguistics and psychology. 

# Introduction 

The recent advances in large language models (LLMs), such as GPT-3~\cite{gpt3}, ChatGPT~\cite{chatgpt}, and LLaMA~\cite{touvron2023llama}, have inspired major breakthroughs in conversational agents. 
Consequently, as an emerging area of interest, numerous applications and algorithms for role-playing conversational agents have been proposed, including Character.AI~\footnote{\url{https://beta.character.ai/}} and  Glow~\footnote{\url{https://www.glowapp.tech/}}, which further endows LLMs with specific personas to meet users' personal demands. 
Previously, significant efforts were required to construct traditional chatbots with specific personalities (e.g., Microsoft's Xiaoice~\citep{xiaoice}). 
However, recent LLMs allow convenient construction of conversational agents displaying distinct personality traits or even personas, simply through prompt engineering.  
Hence, role-playing conversational agents have been increasingly popular and  attracted a wide audience.

Still, analytical studies on role-playing conversational agents remain severely insufficient.
Current conversational agents, while not yet viewed as complete artificial intelligence (AI) for plentiful reasons, can still be perceived from a psychological perspective as classic "stimulus-response" systems.
Consequently, paradigms from psychology can be well adopted to study their behavioral patterns~\citep{butlin2023consciousness, kosinski2023theory}. 
Recent studies have been exploring whether large-scale language models inherently possess specific personality traits~\citep{karra2022estimating, huang2023chatgpt, pan2023llms}, and further attempt to craft conversational agents with designated personality types~\citep{jiang2022evaluating, tu2023characterchat, safdari2023personality}. 
However, existing works primarily focused on personality traits of LLMs in general, instead of role-playing conversational agents, which has been an increasingly important question for their growing application. 

This work aims to investigate whether conversational agents exhibit consistent and expected personalty traits in role-playing scenarios, and introduce a preliminary benchmark test to assess if their portrayed personalities resonate with human perceptions. 
Classic characters from literature or film have established widely recognized  personality impressions among the public. 
It remains an understudied question whether these role-playing chatbots can accurately reproduce these pre-defined personalities, which serves as an indispensable criterion to evaluate their efficacy. 
~\citet{huang2023chatgpt} shows that role-playing LLMs with merely names or descriptions provided as prompts fail to effectively capture the intended personality traits.

There exist several challenges to assess personality traits of role-playing chatbots. 
On one hand, traditional closed-form psychological tests elicit fixed responses like "agree" or "disagree"~\citep{tu2023characterchat, rao2023can}, which might not well represent personality of the target character and even contradict with regular behaviors of role-playing chatbots. 
The contradicting responses might stem from either the underlying LLMs' pre-training data, or simply their shortcomings in text generation such as a lack of step-by-step consideration, especially for smaller LLMs. 
On the other hand, chatbots role-playing specific characters might decline to provide suitable responses, intriguingly, because they accurately mirror some insubordinate characters. This necessitates further prompt engineering to yield  responses that are not only suitable for the tests but also align with the character's persona.

In this paper, our core proposal is to 
analyze personality traits in role-playing conversational agents via an interview-style testing approach. 
For each interviewee character, we designate an experimenter character to pose a series of open-ended questions from our questionnaires.
We devise questionnaires grounded in the Big Five Inventory (BFI) and Myers–Briggs Type Indicator (MBTI) theories. 
This methodology prompts role-playing chatbots to provide open-ended answers that are more consistent with their personas, reflecting their personality traits and speech habits. 
With the question-answer pairs collected, we then apply LLMs to assess their personality types. 
We analyze the personality types of 32 character agents from the ChatHaruhi~\citep{li2023chatharuhi} project. 
By investigating the consistency between BFI personality scores assessed by human psychologists and our approach, we show the efficacy of our assessment framework. 
Then, we collect MBTI personality labels from fan websites for automatic evaluation of personality congruence between role-playing agents and human perception.   
The proposed framework is depicted in the following figure. 

<p align="center">
    <img src="figures/BigfiveEvalPipeline.png">
</p>

In summary, the contributions of this paper are mainly three-fold:

+ We introduce an interview-style framework for personality assessment. 
  It is designed for role-playing chatbots,  
  but potentially applicable to human participants as well.
  This approach uses LLMs to automatically rate participants' personality traits, allowing open-ended and information-rich answers from participants. 
  Through its consistency with human psychologist assessment, we show the effectiveness of our automated assessment framework.

+ To the best of our knowledge, we are the first to study the personality traits in role-playing chatbots.  
  We conduct personality assessments of both BFI and MBTI over 32 role-playing chatbots from ChatHaruhi.
  Experimental results demonstrate that these role-playing agents exhibit diverse personalities consistent with the perception of human audience, suggesting the efficacy of current LLMs and frameworks for role-playing applications.

+ We introduce Haruhi-MBTI, a dataset of MBTI personality labels for 32 characters in ChatHaruhi from fan websites. Haruhi-MBTI, together with ChatHaruhi dataset, serves as the first practical benchmark to evaluate performance of role-playing conversational agents. Hence, we believe Haruhi-MBTI will facilitate future research in this direction.


### Citation

Please cite our paper if you use the data or code in this repo.

```
@misc{wang2023does,
      title={Does Role-Playing Chatbots Capture the Character Personalities? Assessing Personality Traits for Role-Playing Chatbots}, 
      author={Xintao Wang and Quan Tu and Yaying Fei and Ziang Leng and Cheng Li},
      year={2023},
      eprint={2310.17976},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```