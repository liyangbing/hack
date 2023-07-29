#定义一个抽象类
class Chat():

    def ask(self, text):
        pass
    def action(self, text):
        pass

    def chat_stream(self, text, callback):
        pass