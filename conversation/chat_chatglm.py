from transformers import AutoTokenizer, AutoModel

from config.config import *

class ChatGLM():
     
    def __init__(self, model_path=CHAT_MODEL_PATH, num_of_round=10):
        model_path = CHAT_MODEL_PATH
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.num_of_round = num_of_round
        self.history = []

    def ask(self, question):

        self.history.append({"role": "user", "content": question})
        
        question = question_template.format(question)
        result, _ = self.model.chat(self.tokenizer, question, self.history)
        
        self.history.append({"role": "system", "content": result})

        if len(self.history) > self.num_of_round*2 + 1:
                del self.history[1:3]
        return result

def action(self, answer):

    answer = prompt_action_template.format(answer)
    logging.debug("answer: {}".format(answer))
    result, _ = self.model.chat(self.tokenizer, answer, [])
    return result

response = action("滔滔不绝")
print(response)


