
import gradio as gr

import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:3]
        return message

prompt = """你是一个AI直播助手，用中文回答相关问题。你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在100个字以内"""

conv = Conversation(prompt, 10)

def answer(question, history=[]):
    history.append(question)
    response = conv.ask(question)
    history.append(response)
    responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
    print("response:", responses)
    print("history:", history)

    return responses, history

with gr.Blocks(css="#chatbot{height:300px} .overflow-y-auto{height:500px}") as demo:
    chatbot = gr.Chatbot(elem_id="chatxybot")
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)

    txt.submit(answer, [txt, state], [chatbot, state])

demo.launch()