import time
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from config.config import *
from conversation.chat import Chat
import langchain
from langchain.cache import InMemoryCache

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
            llm=OpenAI(),
            prompt=self.promptTemplate,
         #    memory=self.memory,
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
        
    def ask(self, question):
        start_time = time.time()
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


