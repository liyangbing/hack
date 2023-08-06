import torch
import os
import openai
import logging

# env有dev, prod两个值
ENV_DEV = "dev"
ENV_PROD = "prod"

ENV = ENV_PROD

CHAT_MODEL_PATH = "/opt/chatglm-6b"
AUDIO_SAVA_PATH = "/mnt/data/audio"
AUDIO_URL = "http://localhost:50003"
secret_key = "n9qCDwTD"


# chat
CHAT_GLM_35 = "GPT-35"
CHAT_GLM_6B = "GPT-6B"
chat_glm = CHAT_GLM_35


# text 2 audio
VOICE_VITS = "vits"
VOICE_AZURE = "azure"
voice_glm = VOICE_AZURE

whisper_local = False

redis_host = "localhost"
redis_port = 6379
sqllite_db = "./dataset/zhibo/db.sqlite3"
sqllite_db_table = "qa"
qa_jsonl = "./dataset/zhibo/qa.jsonl"
#定义向量距离阈值
distance_threshold = 5



embedding_model_name = "text-embedding-ada-002"
gpt_name = "gpt-35"
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"

question_template = """
    你是一个自然科学家，需要创建一个10页的绘本来解答孩子的问题
    要求如下：
    1、答案要尽可能的全面，从多角度回答
    2、每页需要有一个图像描述和一个相关的文本描述
    3、每页为一个jsonl条目，包括两个字段：'image'（描述绘本中的图像，使用英文）和'text'（描述图像内容和回答孩子的问题，使用中文）
    4、直接给出jsonl答案,不需要注释或解释，答案是可以python解析的
    5、直接进入正题，不要话术

    问题：{}
"""

chat_gpt_question_template = """
    你是一个自然科学家，需要创建一个10页的绘本来解答孩子的问题
    要求如下：
    1、答案要尽可能的全面，从多角度回答
    2、每页需要有一个图像描述和一个相关的文本描述
    3、每页为一个jsonl条目，包括两个字段：'image'（描述绘本中的图像，使用英文）和'text'（描述图像内容和回答孩子的问题，使用中文）
    4、直接给出jsonl答案,不需要注释或解释，答案是可以python解析的
    
    Human: {human_input}
    Chatbot:
"""

prompt_action_template = """
    请根据内容，选择一个对应的英文标签，标签如下：
    welcome
    chuckle
    thinking
    thinking2
    crossarm
    showing
    thanks
    thumbsup
    talk

    文本内容：{}

    请回复对应的英文标签，例如：welcome

"""

chat_gpt_prompt_action_template = """
    请根据内容，选择一个对应的英文标签，标签如下：
    welcome
    chuckle
    thinking
    thinking2
    crossarm
    showing
    thanks
    thumbsup
    talk

    文本内容：{human_input}

    请回复对应的英文标签，例如：welcome

"""

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 设置日志格式
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("watchdog.observers.inotify_buffer").setLevel(logging.WARNING)

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "https://api.openai-proxy.com/v1"


AZURE_SPEECH_KEY = os.environ["AZURE_SPEECH_KEY"]
AZURE_SPEECH_REGION = os.environ["AZURE_SPEECH_REGION"]

OSS_ACCESS_KEY_ID = os.environ["OSS_ACCESS_KEY_ID"]
OSS_ACCESS_KEY_SECRET = os.environ["OSS_ACCESS_KEY_SECRET"]
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
OSS_BUCKET = 'lyb123'
OSS_PREFIX = 'ai-baby/'


