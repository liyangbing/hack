import json
import re
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import SpacyTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationBufferWindowMemory


llm = OpenAI(temperature=0)
loader = TextLoader('../dataset/assistant_qa.txt')
documents = loader.load()
text_splitter = SpacyTextSplitter(chunk_size=256, pipeline="zh_core_web_sm")
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(texts, embeddings)

faq_chain = VectorDBQA.from_chain_type(llm=OpenAI(
    temperature=0), vectorstore=docsearch, verbose=True)


ORDER_1 = "20230101ABC"
ORDER_2 = "20230101EFG"

ORDER_1_DETAIL = {
    "order_number": ORDER_1,
    "status": "已发货",
    "shipping_date": "2023-01-03",
    "estimated_delivered_date": "2023-01-05",
}

ORDER_2_DETAIL = {
    "order_number": ORDER_2,
    "status": "未发货",
    "shipping_date": None,
    "estimated_delivered_date": None,
}


def search_order(input: str) -> str:
    """
    一个帮助用户查询最新订单状态的工具，并且能处理以下情况：
    1. 在用户没有输入订单号的时候，会询问用户订单号
    2. 在用户输入的订单号查询不到的时候，会让用户二次确认订单号是否正确
    """
    pattern = r"\d+[A-Z]+"
    match = re.search(pattern, input)

    order_number = input
    if match:
        order_number = match.group(0)
    else:
        return "请问您的订单号是多少？"
    if order_number == ORDER_1:
        return json.dumps(ORDER_1_DETAIL)
    elif order_number == ORDER_2:
        return json.dumps(ORDER_2_DETAIL)
    else:
        return f"对不起，根据{input}没有找到您的订单"


def recommend_product(input: str) -> str:
    return "红色连衣裙"


def faq(intput: str) -> str:
    return "7天无理由退货"


tools = [
    Tool(
        name="Search Order", func=search_order, return_direct=True,
        description="useful for when you need to answer questions about customers orders"
    ),
    Tool(name="Recommend Product", func=recommend_product,
         description="useful for when you need to answer questions about product recommendations"
         ),
    Tool(name="FAQ", func=faq,
         description="useful for when you need to answer questions about shopping policies, like return policy, shipping policy, etc."
         )
]

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=10, return_messages=True)
conversation_agent = initialize_agent(tools, OpenAI(temperature=0),
                                      agent="conversational-react-description", memory=memory, max_iterations=2, verbose=True)

def ask(question):
    answer = conversation_agent.run(question)
    return answer   

question = "我有一张订单，订单号是，一直没有收到，能麻烦帮我查一下吗？"
answer = conversation_agent.run(question)
print(answer)

