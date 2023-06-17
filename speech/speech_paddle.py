
from paddlespeech.cli.tts.infer import TTSExecutor

tts_executor = TTSExecutor()

text = "今天天气十分不错，百度也能做语音合成。"
output_file = "../dataset/paddlespeech.wav"
tts_executor(text=text, output=output_file)

import os
os.environ["AZURE_SPEECH_KEY"] = "90a11485d407439da93a5e68492a985e"
os.environ["AZURE_SPEECH_REGION"] = "eastus"
os.environ["DID_API_KEY"] = "bHliaW5nMzE1QDE2My5jb20:SB3Bk8ase4GWQQ-xweYIF"


AZURE_SPEECH_KEY = "90a11485d407439da93a5e68492a985e"
AZURE_SPEECH_REGION = "eastus"