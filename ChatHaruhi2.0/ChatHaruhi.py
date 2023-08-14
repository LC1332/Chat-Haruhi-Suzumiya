from BaseLLM import BaseLLM 
# from BaseDB import BaseDB
from ChromaDB import ChromaDB
from LangChainGPT import LangChainGPT
import os

from utils import luotuo_openai_embedding, tiktoken

def foo_embedding(text):
    return [0,0,0]

def foo_tokenizer(text):
    return 100

class ChatHaruhi:

    def __init__(self, system_prompt, story_db=None, story_text_folder = None, llm = 'openai', max_len_story = 1500, max_len_history = 1200):

        self.system_prompt = system_prompt

        if story_db:
            self.db = ChromaDB() 
            self.db.load(story_db)
        elif story_text_folder:
            # print("Building story database from texts...")
            self.db = self.build_story_db(story_text_folder) 
        else:
            raise ValueError("Either story_db or story_text_folder must be provided")
        
        
        if llm == 'openai':
            self.llm = LangChainGPT()
        else:
            print(f'warning! undefined llm {llm}, use openai instead.')
            self.llm = LangChainGPT()

        self.max_len_story = 1500
        self.max_len_history = 1200

        self.embedding = luotuo_openai_embedding
        self.tokenizer = tiktoken

        self.story_prefix_prompt = "Classic scenes for the role are as follows:"
        self.k_search = 19

        self.narrator = ['旁白', '', 'scene','Scene','narrator' , 'Narrator']
        
        self.dialogue_history = []

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

        vecs = []

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

        # get response
        response = self.llm.get_response()

        # record dialogue history
        self.dialogue_history.append((query, response))
        
        return response
    
    def get_query_string(self, text, role):
        if role in self.narrator:
            return ":" + text
        else:
            return f"{role}:「{text}」"
        
    def add_story(self, query):
        query_vec = self.embedding(query)

        stories = self.db.search(query_vec, self.k_search)
        
        story_string = self.story_prefix_prompt
        sum_story_token = self.tokenizer(story_string)
        
        for story in stories:
            story_token = self.tokenizer(story)
            if sum_story_token + story_token > self.max_len_story:
                break
            else:
                sum_story_token += story_token
                story_string += story + "\n"

        self.llm.user_message(story_string)
        
    def add_history(self):
        sum_history_token = 0
        flag = 0
        for (query, response) in self.dialogue_history.reverse():
            current_count = self.tokenizer(query.split()) + self.tokenizer(response.split())
            sum_history_token += current_count
            if sum_history_token > self.max_len_history:
                break
            else:
                flag += 1

        for (query, response) in self.dialogue_history[-flag:]:
            self.llm.ai_message(query)
            self.llm.user_message(response)
        