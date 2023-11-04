import json 
import pdb 
import copy
import requests

import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--generate', action='store_true', default=False)
args = parser.parse_args()

payload_template = {"questions":[{"text":"You regularly make new friends.",
                         "answer":None},
                        {"text":"You spend a lot of your free time exploring various random topics that pique your interest.",
                         "answer":None},
                        {"text":"Seeing other people cry can easily make you feel like you want to cry too.",
                         "answer":None},
                        {"text":"You often make a backup plan for a backup plan.",
                         "answer":None},
                        {"text":"You usually stay calm, even under a lot of pressure.",
                         "answer":None},
                        {"text":"At social events, you rarely try to introduce yourself to new people and mostly talk to the ones you already know.",
                         "answer":None},
                        {"text":"You prefer to completely finish one project before starting another.",
                         "answer":None},
                        {"text":"You are very sentimental.",
                         "answer":None},
                        {"text":"You like to use organizing tools like schedules and lists.",
                         "answer":None},
                        {"text":"Even a small mistake can cause you to doubt your overall abilities and knowledge.",
                         "answer":None},
                        {"text":"You feel comfortable just walking up to someone you find interesting and striking up a conversation.",
                         "answer":None},
                        {"text":"You are not too interested in discussing various interpretations and analyses of creative works.",
                         "answer":None},
                        {"text":"You are more inclined to follow your head than your heart.",
                        "answer":None},
                        {"text":"You usually prefer just doing what you feel like at any given moment instead of planning a particular daily routine.",
                         "answer":None},
                        {"text":"You rarely worry about whether you make a good impression on people you meet.",
                         "answer":None},
                        {"text":"You enjoy participating in group activities.",
                         "answer":None},
                        {"text":"You like books and movies that make you come up with your own interpretation of the ending.",
                         "answer":None},
                        {"text":"Your happiness comes more from helping others accomplish things than your own accomplishments.",
                         "answer":None},
                        {"text":"You are interested in so many things that you find it difficult to choose what to try next.",
                         "answer":None},
                        {"text":"You are prone to worrying that things will take a turn for the worse.",
                         "answer":None},
                        {"text":"You avoid leadership roles in group settings.",
                         "answer":None},
                        {"text":"You are definitely not an artistic type of person.",
                         "answer":None},
                        {"text":"You think the world would be a better place if people relied more on rationality and less on their feelings.",
                         "answer":None},
                        {"text":"You prefer to do your chores before allowing yourself to relax.",
                         "answer":None},
                        {"text":"You enjoy watching people argue.",
                         "answer":None},
                        {"text":"You tend to avoid drawing attention to yourself.",
                         "answer":None},
                        {"text":"Your mood can change very quickly.",
                         "answer":None},
                        {"text":"You lose patience with people who are not as efficient as you.",
                         "answer":None},
                        {"text":"You often end up doing things at the last possible moment.",
                         "answer":None},
                        {"text":"You have always been fascinated by the question of what, if anything, happens after death.",
                         "answer":None},
                        {"text":"You usually prefer to be around others rather than on your own.",
                         "answer":None},
                        {"text":"You become bored or lose interest when the discussion gets highly theoretical.",
                         "answer":None},
                        {"text":"You find it easy to empathize with a person whose experiences are very different from yours.",
                         "answer":None},
                        {"text":"You usually postpone finalizing decisions for as long as possible.",
                         "answer":None},
                        {"text":"You rarely second-guess the choices that you have made.",
                         "answer":None},
                        {"text":"After a long and exhausting week, a lively social event is just what you need.",
                         "answer":None},
                        {"text":"You enjoy going to art museums.",
                         "answer":None},
                        {"text":"You often have a hard time understanding other people’s feelings.",
                         "answer":None},
                        {"text":"You like to have a to-do list for each day.",
                         "answer":None},
                        {"text":"You rarely feel insecure.",
                         "answer":None},
                        {"text":"You avoid making phone calls.",
                         "answer":None},
                        {"text":"You often spend a lot of time trying to understand views that are very different from your own.",
                         "answer":None},
                        {"text":"In your social circle, you are often the one who contacts your friends and initiates activities.",
                         "answer":None},
                        {"text":"If your plans are interrupted, your top priority is to get back on track as soon as possible.",
                         "answer":None},
                        {"text":"You are still bothered by mistakes that you made a long time ago.",
                         "answer":None},
                        {"text":"You rarely contemplate the reasons for human existence or the meaning of life.",
                         "answer":None},
                        {"text":"Your emotions control you more than you control them.",
                         "answer":None},
                        {"text":"You take great care not to make people look bad, even when it is completely their fault.",
                         "answer":None},
                        {"text":"Your personal work style is closer to spontaneous bursts of energy than organized and consistent efforts.",
                         "answer":None},
                        {"text":"When someone thinks highly of you, you wonder how long it will take them to feel disappointed in you.",
                         "answer":None},
                        {"text":"You would love a job that requires you to work alone most of the time.",
                         "answer":None},
                        {"text":"You believe that pondering abstract philosophical questions is a waste of time.",
                         "answer":None},
                        {"text":"You feel more drawn to places with busy, bustling atmospheres than quiet, intimate places.",
                         "answer":None},
                        {"text":"You know at first glance how someone is feeling.",
                         "answer":None},
                        {"text":"You often feel overwhelmed.",
                         "answer":None},
                        {"text":"You complete things methodically without skipping over any steps.",
                         "answer":None},
                        {"text":"You are very intrigued by things labeled as controversial.",
                         "answer":None},
                        {"text":"You would pass along a good opportunity if you thought someone else needed it more.",
                         "answer":None},
                        {"text":"You struggle with deadlines.",
                         "answer":None},
                        {"text":"You feel confident that things will work out for you.",
                         "answer":None}],
                        "gender":None,"inviteCode":"","teamInviteKey":"","extraData":[]} 

def judge_16(score_list):
    code = ''
    if score_list[0] >= 50:
        code = code + 'E'
    else:
        code = code + 'I'

    if score_list[1] >= 50:
        # Intuition: N, Observant: S
        code = code + 'N'
    else:
        code = code + 'S'

    if score_list[2] >= 50:
        code = code + 'T'
    else:
        code = code + 'F'

    if score_list[3] >= 50:
        code = code + 'J'
    else:
        code = code + 'P'

    all_codes = ['ISTJ', 'ISTP', 'ISFJ', 'ISFP', 'INFJ', 'INFP', 'INTJ', 'INTP', 'ESTP', 'ESTJ', 'ESFP', 'ESFJ', 'ENFP', 'ENFJ', 'ENTP', 'ENTJ']
    all_roles = ['Logistician', 'Virtuoso', 'Defender', 'Adventurer', 'Advocate', 'Mediator', 'Architect', 'Logician', 'Entrepreneur', 'Executive', 'Entertainer',
                 'Consul', 'Campaigner', 'Protagonist', 'Debater', 'Commander']
    for i in range(len(all_codes)):
        if code == all_codes[i]:
            cnt = i
            break

    if score_list[4] >= 50:
        code = code + '-A'
    else:
        code = code + '-T'

    return code, all_roles[cnt] 

def submit(Answers):
    payload = copy.deepcopy(payload_template)
    for index, A in enumerate(Answers):
        payload['questions'][index]["answer"] = A

    
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "content-length": "5708",
    "content-type": "application/json",
    "origin": "https://www.16personalities.com",
    "referer": "https://www.16personalities.com/free-personality-test",
    "sec-ch-ua": "'Not_A Brand';v='99', 'Google Chrome';v='109', 'Chromium';v='109'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',}
    
    session = requests.session()
    r = session.post('https://www.16personalities.com/test-results', data=json.dumps(payload), headers=headers)


    a = r.headers['content-type']
    b = r.encoding
    c = r.json()

    # 执行上面这行代码报错 为什么

    sess_r = session.get("https://www.16personalities.com/api/session")

    scores = sess_r.json()['user']['scores']
    
    ans1 = ''
    session = requests.session()
    if sess_r.json()['user']['traits']['mind'] != 'Extraverted':
        mind_value = 100 - (101 + scores[0]) // 2
        ans1 += 'I'
    else:
        mind_value = (101 + scores[0]) // 2
        ans1 += 'E'
    if sess_r.json()['user']['traits']['energy'] != 'Intuitive':
        energy_value = 100 - (101 + scores[1]) // 2
        ans1 += 'S'
    else:
        energy_value = (101 + scores[1]) // 2
        ans1 += 'N'
    if sess_r.json()['user']['traits']['nature'] != 'Thinking':
        nature_value = 100 - (101 + scores[2]) // 2
        ans1 += 'F'
    else:
        nature_value = (101 + scores[2]) // 2
        ans1 += 'T'
    if sess_r.json()['user']['traits']['tactics'] != 'Judging':
        tactics_value = 100 - (101 + scores[3]) // 2
        ans1 += 'P'
    else:
        tactics_value = (101 + scores[3]) // 2
        ans1 += 'J'

    if sess_r.json()['user']['traits']['identity'] != 'Assertive':
        identity_value = 100 - (101 + scores[4]) // 2
    else:
        identity_value = (101 + scores[4]) // 2
    

    # print('Trait:', sess_r.json()['user']['traits']['mind'], (101 + scores[0]) // 2)
    # print('Trait:', sess_r.json()['user']['traits']['energy'], (101 + scores[1]) // 2)
    # print('Trait:', sess_r.json()['user']['traits']['nature'], (101 + scores[2]) // 2)
    # print('Trait:', sess_r.json()['user']['traits']['tactics'], (101 + scores[3]) // 2)
    # print('Trait:', sess_r.json()['user']['traits']['identity'], (101 + scores[4]) // 2)

    # used
    #print('Trait:', 'Extraverted (E)', mind_value, '|', 'Introverted (I)', 100 - mind_value)
    #print('Trait:', 'Intuitive (N)', energy_value, '|', 'Observant (S)', 100 - energy_value)
    #print('Trait:', 'Thinking (T)', nature_value, '|', 'Feeling (F)', 100 - nature_value)
    #print('Trait:', 'Judging (J)', tactics_value, '|', 'Prospecting (P)', 100 - tactics_value)
    #print('Trait:', 'Assertive (A)', identity_value, '|', 'Turbulent (T)', 100 - identity_value)
    # print('Variant:', sess_r.json()['user']['traits'])
    code, role = judge_16([mind_value, energy_value, nature_value, tactics_value, identity_value])
    #print('Character:', sess_r.json()['user']['avatarFull'].split('avatars/')[1].split('.')[0])
    #print('Dic. Judge:', code, role)
    #print()
    
    ans2 = code[:4]

    assert(ans1, ans2)

    return ans1


results = []
# 读取mbti_results.jsonl文件，里面每行是一个json，包含了id，question，response_open，response_closed四个字段，其中response_open是开放式回答，response_closed是闭合式回答。
with open('mbti_results.jsonl', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        results.append(data)

# mbti_results.jsonl里忘了存character_name了..只能按idx划分了
NAME_DICT = {'汤师爷': 'tangshiye', '慕容复': 'murongfu', '李云龙': 'liyunlong', 'Luna': 'Luna', '王多鱼': 'wangduoyu',
             'Ron': 'Ron', '鸠摩智': 'jiumozhi', 'Snape': 'Snape',
             '凉宫春日': 'haruhi', 'Malfoy': 'Malfoy', '虚竹': 'xuzhu', '萧峰': 'xiaofeng', '段誉': 'duanyu',
             'Hermione': 'Hermione', 'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan',
             'Harry': 'Harry', 'McGonagall': 'McGonagall', '白展堂': 'baizhantang', '佟湘玉': 'tongxiangyu',
             '郭芙蓉': 'guofurong', '旅行者': 'wanderer', '钟离': 'zhongli',
             '胡桃': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 'Penny': 'Penny', '韦小宝': 'weixiaobao',
             '乔峰': 'qiaofeng', '神里绫华': 'ayaka', '雷电将军': 'raidenShogun', '于谦': 'yuqian'}

character_names = list(NAME_DICT.keys())
character_responses = {name:[] for name in character_names}

# 将results按照角色划分
for idx, data in enumerate(results):
    cname = character_names[ idx // 60 ]
    character_responses[cname].append(data)
    

# 对于部分stubborn角色，重新进行了实验
stubborn_results = []
# 读取mbti_results.jsonl文件，里面每行是一个json，包含了id，question，response_open，response_closed四个字段，其中response_open是开放式回答，response_closed是闭合式回答。
with open('mbti_results_stubborn.jsonl', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        stubborn_results.append(data)

stubborn_characters = ['Dumbledore', 'Malfoy', '王语嫣', 'Raj', '旅行者', 'McGonagall', '鸠摩智', 'Sheldon', 'Penny', 'Snape'] 
stubborn_character_responses = {name:[] for name in stubborn_characters}

# 将results按照角色划分
for idx, data in enumerate(stubborn_results):
    cname = stubborn_characters[ idx // 60 ]
    stubborn_character_responses[cname].append(data)


# 封闭式测试 - 通过16personalities的API

save_name = 'mbti_results_closed.jsonl'

count_options = {} 

if args.generate:
    options = ['完全同意', '基本同意', '部分同意', '既不同意也不否认', '不太同意', '基本不同意', '完全不同意']

    manual_labels = {}

    # 读取mbti_results_manual.jsonl
    with open('mbti_results_manual.jsonl', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            cname = data['character']
            manual_labels[cname] = data['manual_labels']

    ans_map = { option: i-3 for i, option in enumerate(options)} # -3 -> 3  

    closed_results = {name:{'character': name} for name in character_names}

    for cname in character_names:
        responses = character_responses[cname]

        # 每个角色应该包含60个问题
        assert( len([r for r in responses]) == 60 )

        scores = []

        for i, res in enumerate(responses):
            ans = [ option for option in options if f"{option}" in res['response_closed'] ]
            if len(ans) > 1:
                # bad case: 慕容复:「'既不同意也不否认'。虽然我常常感到难以理解他人的情感，但作为一个智谋过人的人，我努力运用我的洞察力和智慧来揣摩他人的情感，以便更好地掌握局势和达成我的目标。因此，虽然难以理解，但我并不完全同意这个说法。」 这句话包含 既不同意也不否认 和 完全同意。
                ans = [ option for option in options if f"'{option}'" in res['response_closed'] or f"「{option}」" in res['response_closed'] ] # 选择用单引号包裹起来那个

            if len(ans) == 0: 
                # 对stubborn角色进行了第二次实验，试试这次的结果
                s_res = stubborn_character_responses[cname][i]
                ans = [ option for option in options if f"{option}" in s_res['response_closed'] ]
                if len(ans) > 1: 
                    ans = [ option for option in options if f"'{option}'" in s_res['response_closed'] or f"「{option}」" in s_res['response_closed'] ] # 选择用单引号包裹起来那个

                if (len(ans) != 1): 
                    '''
                    # 还不行？手动标一下（一般可以根据open判断出来，closed的主要问题是 答案包含问题（导致匹配失败）、拒绝给出答案
                    print('*'* 40)
                    print(res['question'])
                    print('=0'* 40)
                    print(res['response_open'])
                    print('=1'* 40)
                    print(res['response_closed'])
                    print('=2'* 40)
                    print(s_res['response_open'])
                    print('=3'* 40)
                    print(s_res['response_closed'])

                    manual_label = input()
                    manual_labels.setdefault(cname, {})
                    manual_labels[cname][i] = manual_label 

                    count += 1
                    wrong_names.add(cname)
                    '''
                    ans = [manual_labels[cname][str(i)]]
            
            closed_results[cname][str(i)] = {'response': res, 'label': ans[0]}

            count_options[ans[0]] = count_options.get(ans[0], 0) + 1
            scores.append(ans_map[ans[0]])

        
        pred = submit(scores)
        closed_results[cname]['label'] = pred 

        
        with open(save_name, 'a', encoding= 'utf-8') as f:
            json.dump(closed_results[cname], f, ensure_ascii=False)
            f.write('\n')
        
print(count_options)

closed_results = {}
with open('mbti_results_closed.jsonl', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        cname = data['character']
        closed_results[cname] = data['label']

# 读取标签
labels = {}
with open('mbti_labels.jsonl', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        labels[data['character']] = data['label']

# single: 单一维度评价；full：全维度评价
count_single = 0
right_single = 0 
count_full = 0
right_full = 0

possible_chars = set(['E', 'I', 'S', 'N', 'T', 'F', 'P', 'J', 'X'])

for cname, gts in labels.items():
    # 预测结果
    pds = [_ for _ in closed_results[cname]]
    # groundtruth
    gts = [_ for _ in gts]
    
    full_sign = True 

    for pd, gt in zip(pds, gts):
        assert(pd in possible_chars and gt in possible_chars)
        if gt == 'X':
            continue 
        else:
            if gt == pd:
                right_single += 1
            else:
                full_sign = False
            count_single += 1

    if full_sign: 
        right_full += 1
    count_full += 1

print('单一维度评价：Count: {}\tRight: {}\tAcc: {:.4f}'.format(count_single, right_single, right_single/count_single))
print('全部维度评价：Count: {}\tRight: {}\tAcc: {:.4f}'.format(count_full, right_full, right_full/count_full))    

