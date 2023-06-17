import base64
import io
import time
import whisper
import librosa
import sys
sys.path.append("../")
from config.config import *

AUDIO_SAVA_PATH = "./"
 # 解码 base64 编码的音频

path = "../dataset/tts.mp3"
with open(path, "rb") as wav_file:
    wav_data = wav_file.read()
    base64_data = base64.b64encode(wav_data)
    decoded_audio = base64.b64decode(base64_data)

# AUDIO_SAVA_PATH, 时间戳，生成文件名
out_file = f"{AUDIO_SAVA_PATH}/{int(time.time())}.mp3"
with open(out_file, "wb") as f:
        f.write(decoded_audio)

model = whisper.load_model("base")
result = model.transcribe(out_file)
print(result["text"])