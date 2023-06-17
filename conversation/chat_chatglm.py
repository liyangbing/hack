import time
from transformers import AutoTokenizer, AutoModel

from config.config import *
from conversation.chat import Chat

class ChatGLM6B(Chat):
     
    def __init__(self, model_path=CHAT_MODEL_PATH, num_of_round=10):
        model_path = CHAT_MODEL_PATH
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.num_of_round = num_of_round
        self.history = []

    def ask(self, question):
        self.history.append({"role": "user", "content": question})
        
        start_time = time.time()
        question = question_template.format(question)
        answer, _ = self.model.chat(self.tokenizer, question, self.history)
        end_time = time.time()
        logging.debug("ChatGLM6B ask elase time: %s秒, question: %s, answer: %s", end_time - start_time, question, answer)

        self.history.append({"role": "system", "content": answer})

        if len(self.history) > self.num_of_round*2 + 1:
                del self.history[1:3]
        return answer

    def action(self, answer):
        start_time = time.time()
        answer = prompt_action_template.format(answer)
        result, _ = self.model.chat(self.tokenizer, answer, [])
        end_time = time.time()
        logging.debug("ChatGLM6B action elase time: %s秒, answer: %s, action: %s", end_time - start_time, answer, result)
        return result


