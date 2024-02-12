import os

from .BaseLLM import BaseLLM

zhipu_api = os.environ['ZHIPU_API']

from zhipuai import ZhipuAI
import time

FAIL = "FAIL"
SUCCESS = "SUCCESS"
PROCESSING = "PROCESSING"


class GLMAPI(BaseLLM):
    def __init__(self, model="glm-3-turbo", verbose=False):
        super(GLMAPI, self).__init__()

        self.client = ZhipuAI(api_key=zhipu_api)

        self.verbose = verbose

        self.model_name = model

        self.prompts = []

        if self.verbose == True:
            print('model name, ', self.model_name)
            if len(zhipu_api) > 8:
                print('found apikey ', zhipu_api[:4], '****', zhipu_api[-4:])
            else:
                print('found apikey but too short, ')

    def initialize_message(self):
        self.prompts = []

    def ai_message(self, payload):
        self.prompts.append({"role": "assistant", "content": payload})

    def system_message(self, payload):
        self.prompts.append({"role": "user", "content": payload})

    def user_message(self, payload):
        self.prompts.append({"role": "user", "content": payload})

    def get_response(self):
        max_test_name = 5
        sleep_interval = 3

        response_id = None

        # try submit asychonize request until success
        for test_time in range(max_test_name):
            response = self.client.chat.asyncCompletions.create(
                model=self.model_name,  # 填写需要调用的模型名称
                messages=self.prompts,
            )
            if response.task_status != FAIL:
                response_id = response.id

                if self.verbose:
                    print("model name : ", response.model)
                    print('submit request, id = ', response_id)
                break
            else:
                print('submit GLM request failed, retrying...')
                time.sleep(sleep_interval)

        if response_id:
            # try get response until success
            for test_time in range(2 * max_test_name):
                result = self.client.chat.asyncCompletions.retrieve_completion_result(id=response_id)

                if result.task_status == FAIL:
                    if self.verbose:
                        print('response id : ', response_id, "task is fail")
                    break

                if result.task_status == PROCESSING:
                    if self.verbose:
                        print('response id : ', response_id, "task is processing")
                    time.sleep(sleep_interval)
                    continue

                # 成功
                if self.verbose:
                    print(
                        f"prompt tokens:{result.usage.prompt_tokens} completion tokens:{result.usage.completion_tokens}")
                    print(f"choices:{result.choices}")
                    print(f"result:{result}")

                return result.choices[-1].message.content

        print('submit GLM request failed, please check your api key and model name')
        return ''

    def print_prompt(self):
        for message in self.prompts:
            print(f"{message['role']}: {message['content']}")
