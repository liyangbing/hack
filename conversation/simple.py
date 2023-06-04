
# -*- coding: utf-8 -*-

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


if __name__ == "__main__":

    prompt = """你是一个程序员，用中文回答相关问题。你的回答需要满足以下要求:
    1. 你的回答必须是中文
    2. 回答限制在100个字以内"""
    conv1 = Conversation(prompt, 7)
    question1 = "你是谁？"
    print("User : %s" % question1)
    print("Assistant : %s\n" % conv1.ask(question1))

    question2 = "世界上最好的语言是什么？"
    print("User : %s" % question2)
    print("Assistant : %s\n" % conv1.ask(question2))

    question3 = "中国有多少程序员？"
    print("User : %s" % question3)
    print("Assistant : %s\n" % conv1.ask(question3))

    question4 = "我问你的第一个问题是什么？"
    print("User : %s" % question4)
    print("Assistant : %s\n" % conv1.ask(question4))

    question5 = "我问你的第一个问题是什么？"
    print("User : %s" % question5)
    print("Assistant : %s\n" % conv1.ask(question5))
