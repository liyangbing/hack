import time
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from config import config
from config.config import *
from conversation.chat import Chat
import langchain
from langchain.cache import InMemoryCache
from database.faiss_qa_db import FaissQAIndex
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


from database.sqllite_db import SQLiteDB

# 定义一个函数来检查字符串是否包含一个断句的标点符号
def contains_sentence_break(s):
    sentence_breaks = ['!', '?', '\n', '，', '。', '！', '？', '\n']
    return any(break_char in s for break_char in sentence_breaks)

class ChatSimpleGPT(Chat):

    def __init__(self, num_of_round=10):
        self.num_of_round = num_of_round
        self.promptTemplate = PromptTemplate(
            # input_variables=["chat_history", "human_input"],
            input_variables=["human_input"],

            template=chat_gpt_question_template
        )
        langchain.llm_cache = InMemoryCache()
        logging.debug("cache ChatSimpleGPT init")
        # self.memory = ConversationBufferWindowMemory(memory_key="chat_history", k=num_of_round)
        self.llm_chain = LLMChain(
            llm=OpenAI(max_tokens=1024),
            prompt=self.promptTemplate,
         #    memory=self.memory,
            verbose=True
        )

        self.llm_stream_chain = LLMChain(
            llm=OpenAI(max_tokens=1024,
                       streaming=True,
                       callbacks=[StreamingStdOutCallbackHandler()]
                       ),
            prompt=self.promptTemplate,
            verbose=True
        )

        self.action_llm_chain = LLMChain(
            llm=OpenAI(),
            prompt=PromptTemplate(
                input_variables=["human_input"],
                template=chat_gpt_prompt_action_template
            ),
            verbose=True
        )

        logging.info("init vector store,use db: %s", config.sqllite_db)
        self.faiss = self.build_faiss_index()
        
    def ask(self, question):
        start_time = time.time()
        vector_result = self.faiss.search_by_distance(question, config.distance_threshold)
        logging.info("ChatSimpleGPT ask question %s, distance_threshold: %f, vector_result: %s", 
                     question, config.distance_threshold,vector_result)
        # 根据vector_result hit判断是否命中
        if vector_result["hit"]:
            answer = vector_result["answer"]
        else:
            answer = self.llm_chain.predict(human_input=question)
        end_time = time.time()
        logging.debug("ChatSimpleGPT ask elase time: %s秒, question: %s, answer: %s", end_time - start_time, question, answer)
        
        return answer

    def action(self, answer):
        start_time = time.time()
        result = self.action_llm_chain.predict(human_input=answer)
        end_time = time.time()
        logging.debug("ChatSimpleGPT action elase time: %s秒, answer: %s, action: %s", end_time - start_time, answer, result)
        return result
    
    def chat_stream(self, question, callback):
        start_time = time.time()
        vector_result = self.faiss.search_by_distance(question, config.distance_threshold)
        logging.info("ChatSimpleGPT ask question %s, distance_threshold: %f, vector_result: %s", 
                     question, config.distance_threshold,vector_result)
        
        answer = None  

        # 根据vector_result hit判断是否命中
        if vector_result["hit"]:
            answer = vector_result["answer"]
            callback(answer)
        else:
            # send a ChatCompletion request to count to 100
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': question}
                ],
                max_tokens=2048,
                temperature=0,
                stream=True  # again, we set stream=True
            )

            # create variables to collect the stream of chunks
            collected_line_messages = []
            # iterate through the stream of events
            for chunk in response:
                chunk_time = time.time() - start_time
                chunk_message = chunk['choices'][0]['delta']
                collected_line_messages.append(chunk_message)
                if contains_sentence_break(chunk_message.get('content', '')):
                    line_reply_content = ''.join([m.get('content', '') for m in collected_line_messages])

                    print(f"Message received {chunk_time:.2f} seconds after request: {line_reply_content}")
                    callback(line_reply_content)
                    collected_line_messages = []  # 清空收集的消息，以便收集下一组

            if len(collected_line_messages) > 0:
                line_reply_content = ''.join([m.get('content', '') for m in collected_line_messages])
                print(f"Message received {chunk_time:.2f} seconds after request: {line_reply_content}")
                callback(line_reply_content)
        
        end_time = time.time()
        logging.debug("ChatSimpleGPT ask elase time: %s秒, question: %s, answer: %s", end_time - start_time, question, answer)
        return answer

    def build_faiss_index(self):
        db = SQLiteDB(config.sqllite_db)
        faiss_index = FaissQAIndex()
        datas = db.select('qa', columns='question, answer')
        for data in datas:
            faiss_index.add_data(data)
        faiss_index.build_index()
        return faiss_index


