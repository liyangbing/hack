import torch
import os
import openai

# env有dev, prod两个值
ENV_DEV = "dev"
ENV_PROD = "prod"

ENV = ENV_DEV

CHAT_MODEL_PATH = "/Users/lyb/code/aitest/chatglm-6b"
AUDIO_SAVA_PATH = "/Users/lyb/code/aitest/hack/audio"
AUDIO_URL = "http://39.98.94.86:50003"

openai_api_key = ""
embedding_model_name = "text-embedding-ada-002"
gpt_name = "gpt-35"
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"


def set_openai():
    openai.api_key = os.environ["OPENAI_API_KEY"]


def set_env():
    os.environ["EMBEDDING_MODEL_NAME"] = embedding_model_name
    os.environ["GPT_NAME"] = gpt_name
    os.environ["EMBEDDING_DEVICE"] = EMBEDDING_DEVICE
    os.environ["OPENAI_API_KEY"] = openai_api_key

    if ENV == ENV_PROD:
        CHAT_MODEL_PATH = "/opt/chatglm-6b"
        AUDIO_SAVA_PATH = "/opt/audio"
        AUDIO_URL = "http://localhost:50003"

# You can then call these functions with appropriate parameters:
if __name__ == "__main__":

    set_openai(openai_api_key)
    set_env()
