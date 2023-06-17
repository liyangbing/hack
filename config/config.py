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

# 是否使用chatgpt
IS_CHATGPT = True

embedding_model_name = "text-embedding-ada-002"
gpt_name = "gpt-35"
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 设置日志格式
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

openai.api_key = os.environ["OPENAI_API_KEY"]