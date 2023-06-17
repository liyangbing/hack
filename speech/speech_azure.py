
import base64
import logging
import os
import time
import azure.cognitiveservices.speech as speechsdk

class SpeechAzure:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), 
                                                    region=os.environ.get('AZURE_SPEECH_REGION'))
        self.speech_region = os.environ.get('AZURE_SPEECH_REGION')
        self.speech_synthesis_voice_name = 'zh-CN-XiaohanNeural'
        self.speech_config.speech_synthesis_voice_name='zh-CN-XiaohanNeural'


    def text_2_audio(self, text):
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        start_time = time.time()
        result = speech_synthesizer.speak_text_async(text).get()
        stream =speechsdk.AudioDataStream(result)
        end_time = time.time()
        logging.debug("SpeechAzure text_2_audio elase time: %s秒, text %s", end_time - start_time, text)

        # 定义bytear
        resultBytes = []
        stream.read_data(resultBytes)
        base64_data = base64.b64encode(resultBytes)
        audio_base64_string = base64_data.decode("utf-8")

        return audio_base64_string

    def audio_2_text(self, audio):
        pass