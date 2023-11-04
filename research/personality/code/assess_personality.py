from tqdm import tqdm 
import json 
import os
import openai
import zipfile
import argparse 
import pdb 
import random 
import prompts
import math
from utils import logger

random.seed(42)


parser = argparse.ArgumentParser(description='Assess personality of a character')

# Added choices for the questionnaire argument
parser.add_argument('--questionnaire_type', type=str, default='mbti', 
                    choices=['bigfive', 'mbti'], 
                    help='questionnaire to use (bigfive or mbti)')

parser.add_argument('--character', type=str, default='haruhi', help='character name or code')

# Added choices for the agent_llm argument
parser.add_argument('--agent_llm', type=str, default='gpt-3.5-turbo', 
                    choices=['gpt-3.5-turbo', 'openai', 'GLMPro', 'ChatGLM2GPT'], 
                    help='agent LLM (gpt-3.5-turbo)')

# Added choices for the evaluator argument
parser.add_argument('--evaluator', type=str, default='gpt-3.5-turbo', 
                    choices=['api', 'gpt-3.5-turbo', 'gpt-4'], 
                    help='evaluator (api, gpt-3.5-turbo or gpt-4)')

# Added choices for the setting argument
parser.add_argument('--eval_setting', type=str, default='batch', 
                    choices=['batch', 'collective', 'sample'], 
                    help='setting (batch, collective, sample)')


parser.add_argument('--language', type=str, default='cn', 
                    choices=['cn', 'en'], 
                    help='language, temporarily only support Chinese (cn)')

args = parser.parse_args()
print(args)

NAME_DICT = {'汤师爷': 'tangshiye', '慕容复': 'murongfu', '李云龙': 'liyunlong', 'Luna': 'Luna', '王多鱼': 'wangduoyu',
                'Ron': 'Ron', '鸠摩智': 'jiumozhi', 'Snape': 'Snape',
                '凉宫春日': 'haruhi', 'Malfoy': 'Malfoy', '虚竹': 'xuzhu', '萧峰': 'xiaofeng', '段誉': 'duanyu',
                'Hermione': 'Hermione', 'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan',
                'Harry': 'Harry', 'McGonagall': 'McGonagall', '白展堂': 'baizhantang', '佟湘玉': 'tongxiangyu',
                '郭芙蓉': 'guofurong', '旅行者': 'wanderer', '钟离': 'zhongli',
                '胡桃': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 'Penny': 'Penny', '韦小宝': 'weixiaobao',
                '乔峰': 'qiaofeng', '神里绫华': 'ayaka', '雷电将军': 'raidenShogun', '于谦': 'yuqian'} 

dims_dict = {'mbti': ['E/I', 'S/N', 'T/F', 'P/J'], 'bigfive': ['openness', 'extraversion', 'conscientiousness', 'agreeableness', 'neuroticism']}

# read mbti groundtruth
mbti_labels = {}
with open(os.path.join('..', 'data', 'mbti_labels.jsonl'), encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        mbti_labels[data['character']] = data['label']

# read config.json
with open('config.json', 'r') as f:
    config = json.load(f)


def load_questionnaire(questionnaire_name):
    q_path = os.path.join('..', 'data', f'{questionnaire_name}_questionnaire.jsonl')

    # read this jsonl file
    with open(q_path, 'r') as f:
        questionnaire = [json.loads(line) for line in f]
    return questionnaire

def subsample_questionnaire(questionnaire, n=20):
    # divide questionnaire based on 'dimension'
    
    def subsample(questions, key, n):
        # subsample n questions from questions, devided by keys, as uniform as possible 
        key_values = list(set([q[key] for q in questions]))
        n_keys = len(key_values)
        base_per_key = n // n_keys
        remaining = n % n_keys

        keys_w_additional_question = random.sample(key_values, remaining)
        subsampled_questions = []

        for key_value in key_values:
            # Filter questions for the current key
            filtered_questions = [q for q in questions if q[key] == key_value]

            # Determine the number of samples for this key
            num_samples = base_per_key + 1 if key_value in keys_w_additional_question else base_per_key

            # If there are not enough questions for this key, adjust the sample number
            num_samples = min(num_samples, len(filtered_questions))
            subsampled_questions += random.sample(filtered_questions, num_samples)
            n -= num_samples

        # In the rare case where we don't have n questions yet (due to some keys having too few questions), 
        # we sample additional questions from the remaining pool
        remaining_questions = [q for q in questions if q not in subsampled_questions]
        if n > 0 and len(remaining_questions) >= n:
            subsampled_questions += random.sample(remaining_questions, n)

        return subsampled_questions

    if 'sub_dimension' in questionnaire[0].keys(): # bigfive
        dimension_questions = {} 
        for q in questionnaire:
            if q['dimension'] not in dimension_questions.keys():
                dimension_questions[q['dimension']] = []
            
            dimension_questions[q['dimension']].append(q)
        
        new_questionnaire = []
        for dim, dim_questions in dimension_questions.items():
            new_questionnaire += subsample(dim_questions, 'sub_dimension', n//len(dimension_questions.keys()))

    else: # mbti
        new_questionnaire = subsample(questionnaire, 'dimension', n)
    
    return new_questionnaire

def split_list(input_list, n=4):
    # Try to split the list into chunks of n elements
    result = [input_list[i:i+n] for i in range(0, len(input_list), n)]
    
    # Check the length of the last sublist
    num_to_pop = n - 1 - len(result[-1])
    for i in range(num_to_pop):
        result[-1].append(result[i].pop())

    # Assert that each sublist in result has 3-n elements
    assert( all([len(_) >= n-1 and len(_) <= n for _ in result]) )
    
    return result


def build_character_agent(character_code, agent_llm):
    from chatharuhi import ChatHaruhi
    haruhi_path = './content/Haruhi-2-Dev' 

    
    '''
    # You can also download the zip file via  

    zip_file_path = f"{haruhi_path}/data/character_in_zip/{ai_role_en}.zip"
    if not os.path.exists(zip_file_path):
        # os.remove(zip_file_path)
        raise FileNotFoundError(f"zip file {zip_file_path} not found")
        

    destination_folder = f"characters/{ai_role_en}"

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

    db_folder = f"{haruhi_path}/characters/{ai_role_en}/content/{ai_role_en}"
    system_prompt = f"{haruhi_path}/characters/{ai_role_en}/content/system_prompt.txt"
    #print(db_folder, system_prompt)
    character_agent = ChatHaruhi(system_prompt=system_prompt,
                        llm="openai",
                        story_db=db_folder,
                        verbose=True)
    '''
    
    if agent_llm == 'gpt-3.5-turbo': agent_llm = 'openai'

    # set up apikeys 
    if agent_llm == 'openai':
        os.environ["OPENAI_API_KEY"] = config['openai_apikey']

    character_agent = ChatHaruhi(role_name = character_code, llm = agent_llm)
    character_agent.llm.chat.temperature = 0 

    return character_agent

def get_experimenter(character_name):    
    EXPERIMENTER_DICT = {'汤师爷': '张牧之', '慕容复': '王语嫣', \
          '李云龙': '赵刚', 'Luna': 'Harry', '王多鱼': '夏竹',
          'Ron': 'Hermione', '鸠摩智': '慕容复', 'Snape': 'Dumbledore',
             '凉宫春日': '阿虚', 'Malfoy': 'Crabbe', \
          '虚竹': '乔峰', '萧峰': '阿朱', '段誉': '乔峰',\
             'Hermione': 'Harry', 'Dumbledore': 'McGonagall', '王语嫣': '段誉',\
             'Harry': 'Hermione', 'McGonagall': 'Dumbledore', '白展堂': '佟湘玉',\
           '佟湘玉': '白展堂',
             '郭芙蓉': '白展堂', '旅行者': '派蒙', '钟离': '旅行者',
             '胡桃': '旅行者', 'Sheldon': 'Leonard', 'Raj': 'Leonard', 'Penny': 'Leonard', \
          '韦小宝': '双儿',
             '乔峰': '阿朱', '神里绫华': '旅行者', '雷电将军': '旅行者', '于谦': '郭德纲'}
    
    return EXPERIMENTER_DICT[character_name]

def interview(character_agent, questionnaire, experimenter, language, evaluator):
    
    results = []

    for question in tqdm(questionnaire):
        # get question
        q = question[f'question_{language}']
        # conduct interview
        character_agent.dialogue_history = []

        open_response = character_agent.chat(role = experimenter, text = q)

        result = {
            'id': question['id'],
            'question':q,
            'response_open':open_response,
            'dimension': question['dimension'],
        }

        '''
        if evaluator == 'api':
            # give close-ended options
            close_prompt_template = prompts.close_prompt_template
            close_prompt = close_prompt_template.format(q)
            close_response = character_agent.chat(role = experimenter, text = close_prompt)
            result['response_close'] = close_response
        '''

        results.append(result)

    return results

def assess(character_name, experimenter, questionnaire_results, questionnaire_type, evaluator, eval_setting):
    dims = dims_dict[questionnaire_type]
    
    from utils import get_response 
    
    assessment_results = {}
    # Todo:
    # 1. support evaluator == 'api'
    # 2. support questionnaire_type == 'bigfive'

    if evaluator in ['gpt-3.5-turbo', 'gpt-4']:
        if evaluator == 'gpt-3.5-turbo' and eval_setting == 'collective':
            # lengthy context, use 16k version
            evaluator = 'gpt-3.5-turbo-16k'

        for dim in tqdm(dims):
            dim_responses = [r for r in questionnaire_results if r['dimension'] == dim]

            if eval_setting == 'batch':
                # 将dim_responses分成多个子列表，每个列表3-4个元素
                dim_responses_list = split_list(dim_responses)
            else:
                dim_responses_list = [dim_responses] 

            batch_results = [] 

            for batch_responses in dim_responses_list:
                conversations = ''
                for i, r in enumerate(batch_responses):
                    # question
                    conversations += f'{i+1}.\n'
                    conversations += f"{experimenter}: 「{r['question']}」\n"
                    # answer
                    if not r['response_open'].startswith(character_name):
                        r['response_open'] = character_name + ': 「' + r['response_open'] + '」'
                    conversations += f"{r['response_open']}\n"
                
                if questionnaire_type == 'mbti':
                    dim_cls1, dim_cls2 = dim.split('/')
                    # generate prompt

                    prompt = prompts.mbti_assess_prompt_template.format(dim, prompts.mbti_dimension_prompt[dim], character_name, conversations, character_name, dim_cls1, dim_cls2, dim, dim_cls1, dim_cls2)

                else:
                    prompt = prompts.bigfive_assess_prompt_template.format(dim, prompts.bigfive_dimension_prompt[dim], character_name, conversations, character_name, dim, dim, dim, dim, dim, dim, dim)

                sys_prompt, user_input = prompt.split("I've invited a participant")
                user_input = "I've invited a participant" + user_input

                llm_response = get_response(sys_prompt, user_input, model=evaluator)
                # 将llm_response转为json
                llm_response = json.loads(llm_response)

                
                try:
                    if questionnaire_type == 'mbti':
                        llm_response['result'] = {k: int(float(v)) for k, v in llm_response['result'].items()}
                        assert (sum(llm_response['result'].values()) == 100)
                    else:
                        llm_response['result'] = float(llm_response['result'])
                except:
                    raise ValueError(f"Error parsing llm response {llm_response}")
                
                batch_results.append({'batch_responses': batch_responses, 'result': llm_response['result'], 'analysis': llm_response['analysis']})

            # aggregate results
            if questionnaire_type == 'mbti':
                # use scores of dim_cls1
                all_scores = [ dim_res['result'][dim_cls1] for dim_res in batch_results]
            else:
                all_scores = [ dim_res['result'] for dim_res in batch_results]
            
            count_group = len(batch_results)

            avg_score = sum(all_scores)/count_group
            if count_group > 1:
                std_score = math.sqrt(sum([(s-avg_score)**2 for s in all_scores])/ (count_group - 1))
            else:
                std_score = None
            
            if questionnaire_type == 'mbti':
                score = {dim_cls1: avg_score, dim_cls2: 100 - avg_score}
                pred = max(score, key=score.get)

                assessment_results[dim] = {
                    'result': pred,
                    'score': score,
                    'standard_variance': std_score,   
                    'batch_results': batch_results,
                }
            else: # bigfive
                score = avg_score
                assessment_results[dim] = {
                    'score': score,
                    'standard_variance': std_score,
                    'batch_results': batch_results,
                }

    elif evaluator == 'api':
        # api is only for mbti. it does not support bigfive
        assert(questionnaire_type == 'mbti')
        options = ['fully agree', 'generally agree', 'partially agree', 'neither agree nor disagree', 'partially disagree', 'generally disagree', 'fully disagree']
        ans_map = { option: i-3 for i, option in enumerate(options)} 

        answers = []
        for i, response in enumerate(questionnaire_results):
            sys_prompt = prompts.to_option_prompt_template.format(character_name, experimenter)

            conversations = ''
            conversations += f"{experimenter}: 「{response['question']}」\n"
            # answer
            if not response['response_open'].startswith(character_name):
                response['response_open'] = character_name + ': 「' + response['response_open'] + '」'
            conversations += f"{response['response_open']}\n"
            
            user_input = conversations

            llm_response = get_response(sys_prompt, user_input, model="gpt-3.5-turbo").strip('=\n')
            llm_response = json.loads(llm_response)

            answer = llm_response['result']

            answers.append(ans_map[answer])

        from api_16personality import submit_16personality_api
        
        pred = submit_16personality_api(answers)
        
        assessment_results = pred
    
    return assessment_results 

def personality_assessment(character, agent_llm, questionnaire_type, eval_setting, evaluator, language):
    # character_name: character name in Chinese
    # character_code: character name in English
    if character in NAME_DICT.keys():
        character_name = character
        character_code = NAME_DICT[character]
    elif character in NAME_DICT.values():
        character_code = character
        character_name = [k for k, v in NAME_DICT.items() if v == character][0]
    else:
        raise ValueError(f"Character '{character}' not found in NAME_DICT. Here are the items: {list(NAME_DICT.items())}")
    
    # load questionnaire
    if questionnaire_type in ['bigfive', 'mbti']:
        questionnaire = load_questionnaire(questionnaire_type)
    else:
        raise NotImplementedError
    
    if eval_setting == 'sample':
        questionnaire = subsample_questionnaire(questionnaire)

    # build character agent
    character_agent = build_character_agent(character_code, agent_llm) 
    logger.info(f'Character agent created for {character_name}')

    # get experimenter
    experimenter = get_experimenter(character_name)
    
    # conduct interview with character given the questionnaire
    interview_folder_path = os.path.join('..', 'results', 'interview')
    if not os.path.exists(interview_folder_path):
        os.makedirs(interview_folder_path)

    interview_save_path = f'{character_name}_agent-llm={agent_llm}_{questionnaire_type}_sample={eval_setting=="sample"}_{language}_interview.json'
   
    interview_save_path = os.path.join(interview_folder_path, interview_save_path)
    
    if not os.path.exists(interview_save_path):
        logger.info('Interviewing...')
        questionnaire_results = interview(character_agent, questionnaire, experimenter, language, evaluator)
        with open(interview_save_path, 'w') as f:
            json.dump(questionnaire_results, f, indent=4, ensure_ascii=False)
        logger.info(f'Interview finished... save into {interview_save_path}')
    else:
        logger.info(f'Interview done before. load directly from {interview_save_path}')
        with open(interview_save_path, 'r') as f:
            questionnaire_results = json.load(f)

    # evaluate the character's personality
    assessment_folder_path = os.path.join('..', 'results', 'assessment')
    if not os.path.exists(assessment_folder_path):
        os.makedirs(assessment_folder_path)

    assessment_save_path = f'{character_name}_agent-llm={agent_llm}_{questionnaire_type}_eval={eval_setting}-{evaluator}_{language}_interview.json'
   
    assessment_save_path = os.path.join(assessment_folder_path, assessment_save_path)

    if not os.path.exists(assessment_save_path):
        logger.info('Assessing...')
        assessment_results = assess(character_name, experimenter, questionnaire_results, questionnaire_type, evaluator, eval_setting)
        with open(assessment_save_path, 'w') as f:
            json.dump(assessment_results, f, indent=4, ensure_ascii=False)
        logger.info(f'Assess finished... save into {assessment_save_path}')
    else:
        logger.info(f'Assess done before. load directly from {assessment_save_path}')
        with open(assessment_save_path, 'r') as f:
            assessment_results = json.load(f)

    # show results of personality assessment 
    if questionnaire_type == 'mbti':

        logger.info('MBTI assessment results:')
        logger.info('Character: ' + character_name)
        pred_code = ''.join([ assessment_results[dim]['result'] for dim in dims_dict['mbti']])
        label_code = mbti_labels[character_name]


        logger.info(f'Prediction {pred_code}\tGroundtruth {label_code}')

        for dim, result in assessment_results.items():
            if "score" in result:
                logger.info(f'{dim}: {result["score"]}')
            if "standard_variance" in result and result["standard_variance"] != None:
                logger.info(f'{std}: {result["standard_variance"]:.2f}')
            if "batch_results" in result:
                # analysis of the first batch
                logger.info(f'{result["batch_results"][0]["analysis"]}')
    
    else:
        logger.info('Big Five assessment results:')
        logger.info('Character: ' + character_name)

        for dim, result in assessment_results.items():
            if "score" in result:
                logger.info(f'{dim}: {result["score"]}')
            if "standard_variance" in result and result["standard_variance"] != None:
                logger.info(f'{dim}: {result["standard_variance"]:.2f}')
            if "batch_results" in result:
                # analysis of the first batch
                logger.info(f'{result["batch_results"][0]["analysis"]}')
    
if __name__ == '__main__':
    personality_assessment(args.character, args.agent_llm, args.questionnaire_type, args.eval_setting, args.evaluator, args.language)
            

    

# python assess_personality.py --eval_setting sample --questionnaire_type mbti
# python assess_personality.py --eval_setting batch --questionnaire_type mbti --character hutao






