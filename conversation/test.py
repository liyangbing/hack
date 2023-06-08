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
text_splitter = SpacyTextSplitter(chunk_size=16, chunk_overlap=16, pipeline="zh_core_web_sm")
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(texts, embeddings)


res = docsearch.similarity_search_with_score_by_vector(embeddings.embed_query("你是谁"), 1)

print(res)
