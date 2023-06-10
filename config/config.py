import torch
import os
import openai
import logging

# env有dev, prod两个值
ENV_DEV = "dev"
ENV_PROD = "prod"

ENV = ENV_PROD

CHAT_MODEL_PATH = "/opt/chatglm-6b"
AUDIO_SAVA_PATH = "/opt/audio"
AUDIO_URL = "http://localhost:50003"

openai_api_key = ""
embedding_model_name = "text-embedding-ada-002"
gpt_name = "gpt-35"
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 设置日志格式
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def set_openai():
    openai.api_key = os.environ["OPENAI_API_KEY"]


def set_env():
    os.environ["EMBEDDING_MODEL_NAME"] = embedding_model_name
    os.environ["GPT_NAME"] = gpt_name
    os.environ["EMBEDDING_DEVICE"] = EMBEDDING_DEVICE
    os.environ["OPENAI_API_KEY"] = openai_api_key

    
    
    logging.debug("chat_model_path: %s, audio_save_path: %s, audio_url", CHAT_MODEL_PATH, AUDIO_SAVA_PATH, AUDIO_URL)

# You can then call these functions with appropriate parameters:
if __name__ == "__main__":

    set_openai(openai_api_key)
    set_env()


