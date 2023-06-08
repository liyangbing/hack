import json
import re
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import SpacyTextSplitter
from langchain import LLMChain, OpenAI, VectorDBQA
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferWindowMemory

from langchain.agents import Tool, ZeroShotAgent,AgentExecutor

from langchain.chat_models import ChatOpenAI


llm = OpenAI(temperature=0)
loader = TextLoader('../dataset/assistant_qa.txt')
documents = loader.load()
text_splitter = SpacyTextSplitter(chunk_size=256, pipeline="zh_core_web_sm")
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(texts, embeddings)

faq_chain = VectorDBQA.from_chain_type(llm=OpenAI(
    temperature=0), vectorstore=docsearch, verbose=True)


def faq(intput: str) -> str:
    return faq_chain.run(intput)


tools = [
    Tool(name="FAQ", func=faq,
         description="直播，直播间等直播相关问题"
         )
]

PREFIX = """
你是AI虚拟直播助理思思
你和你的搭档在做一场黑客松直播
语气可以活泼轻松一些
语言要通顺，流畅
请记住你所有的回答都要用中文
"""

prompt_ = ZeroShotAgent.create_prompt(
    tools,
    prefix=PREFIX,
    input_variables=["input", "agent_scratchpad"]
)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=10, return_messages=True)

llm_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt_)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

def ask(question):
    answer = agent_chain.run(question)
    return answer   
