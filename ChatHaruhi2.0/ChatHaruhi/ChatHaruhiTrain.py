from .ChatHaruhi import ChatHaruhi
from .ChromaDB import ChromaDB
from transformers import AutoTokenizer
import os


class ChatHaruhiTrain(ChatHaruhi):
    def add_story_with_expire(self, query):
        if self.db is None:
            print("No vec DB！")
            return
        
        query_vec = self.embedding(query)
        stories = self.db.search(query_vec, self.k_search)

        story_string = self.story_prefix_prompt + self.dialogue_divide_token

        sum_story_token = self.tokenizer(story_string)

        for story in stories:
            if query.strip() in story.strip():
                continue

            story_token = self.tokenizer(story.strip()) + self.tokenizer(self.dialogue_divide_token)
            if sum_story_token + story_token > self.max_len_story:
                break
            else:
                sum_story_token += story_token
                story_string += story.strip() + self.dialogue_divide_token

        self.llm.user_message(story_string)

    def generate_prompt(self, query, history, target):
        # 这里修改下其他超参，不规范删了
        self.k_search = 5
        self.max_len_story = 1500
        self.max_len_history = 1200
        self.story_prefix_prompt = "\nClassic scenes for the role are as follows:"

        self.llm.initialize_message()

        self.llm.system_message(self.system_prompt)

        self.add_story_with_expire(query)

        self.add_history(history)

        self.llm.user_message(query)

        self.llm.user_message(target)

        return self.llm.messages

    def add_history(self, history_list):

        if len(history_list) == 0:
            return

        sum_history_token = 0
        flag = 0
        for history in history_list:
            current_count = 0
            if history is not None:
                current_count += self.tokenizer(history)

            sum_history_token += current_count
            if sum_history_token > self.max_len_history:
                break
            else:
                flag += 1

        if flag == 0:
            print('warning! no history added. the last dialogue is too long.')

        # 是否添加历史前缀，
        history_message = ""
        for history in history_list[-flag:]:
            history_message += history
        self.llm.user_message(history_message)

