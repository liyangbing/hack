from transformers import OpenAiAgent
import os

api_key = os.getenv("OPENAI_API_KEY")
agent = OpenAiAgent(model="text-davinci-003", api_key=api_key)

agent.chat("Transform the picture so that there is a rock in there")
