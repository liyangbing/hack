import base64
import time
from speech.speech import Speech
from requests_toolbelt.multipart.encoder import MultipartEncoder
from config.config import *
import requests
import re
import requests
import random
import string

class SpeechVits(Speech):

    def __init__(self):
        self.id = 133
        self.lang = "zh"
        self.format = "wav"
        self.length = 1
        self.noise = 0.667
        self.noisew = 0.8
        self.max = 30
        self.url = f"{AUDIO_URL}/voice"

    def text_2_audio(self, text):
        fields = {
            "text": text,
            "id": str(self.id),
            "format": self.format,
            "lang": self.lang,
            "length": str(self.length),
            "noise": str(self.noise),
            "noisew": str(self.noisew),
            "max": str(self.max)
        }
        boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))

        m = MultipartEncoder(fields=fields, boundary=boundary)
        headers = {"Content-Type": m.content_type}

        start_time = time.time()
        res = requests.post(url=self.url, data=m, headers=headers)
        end_time = time.time()
        logging.debug("SpeechVits text_2_audio elase time: %s秒, text %s", end_time - start_time, text)
        if res.status_code != 200:
            logging.error("voice_vits: %s", res.text)
            return ""
        
        base64_data = base64.b64encode(res.content)
        audio_base64_string = base64_data.decode("utf-8")

        return audio_base64_string
        
    def audio_2_text(self, audio):
        print("audio2Text")
