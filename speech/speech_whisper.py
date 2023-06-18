
import base64
import time
from speech.speech import Speech
from config.config import *
import whisper

class SpeechWhisper(Speech):
    def __init__(self):
        if whisper_local:
            self.whisper = whisper.load_model("small")

    def text_2_audio(self, text):
        pass

    def audio_2_text(self, audio):
        start_time = time.time()
        decoded_audio = base64.b64decode(audio)
    
        out_file = f"{AUDIO_SAVA_PATH}/{int(time.time())}.wav"
        with open(out_file, "wb") as f:
                f.write(decoded_audio)

        if whisper_local:
            result = self.whisper.transcribe(audio=out_file, initial_prompt="这里是黑客松直播间，你是虚拟数字人思思。")
        else:
            result = openai.Audio.transcribe("whisper-1", out_file)
        prompt = result["text"]

        end_time = time.time()
        logging.debug("SpeechWhisper audio to text, elase time: %s秒, out_file: %s, result: %s,text: %s", end_time - start_time, out_file,  result, result["text"])

        return prompt
