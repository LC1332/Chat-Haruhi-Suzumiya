from .ChromaDB import ChromaDB
from .LangChainGPT import LangChainGPT
import os

from .utils import luotuo_openai_embedding, tiktokenizer

class ChatHaruhi:

    def __init__(self, system_prompt = None, \
                 role_name = None, \
                 story_db=None, story_text_folder = None, \
                 llm = 'openai', \
                 max_len_story = None, max_len_history = None,
                 verbose = False):
        super(ChatHaruhi, self).__init__()
        self.verbose = verbose

        if system_prompt:
            self.system_prompt = self.check_system_prompt( system_prompt )

        # TODO: embedding should be the seperately defined, so refactor this part later
        if llm == 'openai':
            # self.llm = LangChainGPT()
            self.llm, self.embedding, self.tokenizer = self.get_models('openai')
        elif llm == 'debug':
            self.llm, self.embedding, self.tokenizer = self.get_models( 'debug')
        elif llm == 'spark':
            from .SparkGPT import SparkGPT
            self.llm, self.embedding, self.tokenizer = self.get_models( 'spark')
        else:
            print(f'warning! undefined llm {llm}, use openai instead.')
            self.llm, self.embedding, self.tokenizer = self.get_models('openai')

        if role_name:

            from .role_name_to_file import get_folder_role_name
            # correct role_name to folder_role_name
            role_name, url = get_folder_role_name(role_name)

            unzip_folder = f'./temp_character_folder/temp_{role_name}'
            db_folder = os.path.join(unzip_folder, f'content/{role_name}')
            system_prompt = os.path.join(unzip_folder, f'content/system_prompt.txt')

            if not os.path.exists(unzip_folder):
                # not yet downloaded
                # url = f'https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{role_name}.zip'
                import requests, zipfile, io
                r = requests.get(url)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(unzip_folder)

            if self.verbose:
                print(f'loading pre-defined character {role_name}...')
            
            self.db = ChromaDB()
            self.db.load(db_folder)
            self.system_prompt = self.check_system_prompt(system_prompt)

        elif story_db:
            self.db = ChromaDB() 
            self.db.load(story_db)
        elif story_text_folder:
            # print("Building story database from texts...")
            self.db = self.build_story_db(story_text_folder) 
        else:
            self.db = None
            print('warning! database not yet figured out, both story_db and story_text_folder are not inputted.')
            # raise ValueError("Either story_db or story_text_folder must be provided")
        

        self.max_len_story, self.max_len_history = self.get_tokenlen_setting('openai')

        if max_len_history is not None:
            self.max_len_history = max_len_history
            # user setting will override default setting

        if max_len_story is not None:
            self.max_len_story = max_len_story
            # user setting will override default setting

        self.dialogue_history = []

        # constants
        self.story_prefix_prompt = "Classic scenes for the role are as follows:\n"
        self.k_search = 19
        self.narrator = ['旁白', '', 'scene','Scene','narrator' , 'Narrator']
        self.dialogue_divide_token = '\n###\n'
        self.dialogue_bra_token = '「'
        self.dialogue_ket_token = '」'

    def check_system_prompt(self, system_prompt):
        # if system_prompt end with .txt, read the file with utf-8
        # else, return the string directly
        if system_prompt.endswith('.txt'):
            with open(system_prompt, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return system_prompt
    

    def get_models(self, model_name):

        # TODO: if output only require tokenizer model, no need to initialize llm
        
        # return the combination of llm, embedding and tokenizer
        if model_name == 'openai':
            return (LangChainGPT(), luotuo_openai_embedding, tiktokenizer)
        elif model_name == 'debug':
            from .PrintLLM import PrintLLM
            return (PrintLLM(), luotuo_openai_embedding, tiktokenizer)
        elif model_name == 'spark':
            return (SparkGPT(), luotuo_openai_embedding, tiktokenizer)
        else:
            print(f'warning! undefined model {model_name}, use openai instead.')
            return (LangChainGPT(), luotuo_openai_embedding, tiktokenizer)
        
    def get_tokenlen_setting( self, model_name ):
        # return the setting of story and history token length
        if model_name == 'openai':
            return (1500, 1200)
        else:
            print(f'warning! undefined model {model_name}, use openai instead.')
            return (1500, 1200)
        
    def build_story_db_from_vec( self, texts, vecs ):
        self.db = ChromaDB()

        self.db.init_from_docs( vecs, texts)

    def build_story_db(self, text_folder):
        # 实现读取文本文件夹,抽取向量的逻辑
        db = ChromaDB()

        strs = []

        # scan all txt file from text_folder
        for file in os.listdir(text_folder):
            # if file name end with txt
            if file.endswith(".txt"):
                file_path = os.path.join(text_folder, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    strs.append(f.read())

        if self.verbose:
            print(f'starting extract embedding... for { len(strs) } files')

        vecs = []

        ## TODO: 建立一个新的embedding batch test的单元测试
        ## 新的支持list batch test的embedding代码
        ## 用新的代码替换下面的for循环
        ## Luotuo-bert-en也发布了，所以可以避开使用openai
        
        for mystr in strs:
            vecs.append(self.embedding(mystr))

        db.init_from_docs(vecs, strs)

        return db
    
    def save_story_db(self, db_path):
        self.db.save(db_path)
        
    def chat(self, text, role):
        # add system prompt
        self.llm.initialize_message()
        self.llm.system_message(self.system_prompt)
    

        # add story
        query = self.get_query_string(text, role)
        self.add_story( query )

        # add history
        self.add_history()

        # add query
        self.llm.user_message(query)
        
        # get response
        response = self.llm.get_response()

        # record dialogue history
        self.dialogue_history.append((query, response))



        return response
    
    def get_query_string(self, text, role):
        if role in self.narrator:
            return ":" + text
        else:
            return f"{role}:{self.dialogue_bra_token}{text}{self.dialogue_ket_token}"
        
    def add_story(self, query):

        if self.db is None:
            return
        
        query_vec = self.embedding(query)

        stories = self.db.search(query_vec, self.k_search)
        
        story_string = self.story_prefix_prompt
        sum_story_token = self.tokenizer(story_string)
        
        for story in stories:
            story_token = self.tokenizer(story) + self.tokenizer(self.dialogue_divide_token)
            if sum_story_token + story_token > self.max_len_story:
                break
            else:
                sum_story_token += story_token
                story_string += story + self.dialogue_divide_token

        self.llm.user_message(story_string)
        
    def add_history(self):

        if len(self.dialogue_history) == 0:
            return
        
        sum_history_token = 0
        flag = 0
        for query, response in reversed(self.dialogue_history):
            current_count = self.tokenizer(query) 
            current_count += self.tokenizer(response)
            sum_history_token += current_count
            if sum_history_token > self.max_len_history:
                break
            else:
                flag += 1

        if flag == 0:
            print('warning! no history added. the last dialogue is too long.')

        for (query, response) in self.dialogue_history[-flag:]:
            self.llm.user_message(query)
            self.llm.ai_message(response)

        
        
