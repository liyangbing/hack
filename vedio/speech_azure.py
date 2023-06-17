
import os
import time
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = "90a11485d407439da93a5e68492a985e"
AZURE_SPEECH_REGION = "eastus"

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region=os.environ.get('AZURE_SPEECH_REGION'))

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='zh-CN-XiaohanNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

text = "今天天气真不错，ChatGPT真好用。"

result = speech_synthesizer.speak_text_async(text).get()
stream =speechsdk.AudioDataStream(result)

filename = AUDIO_SAVA_PATH + str(int(time.time())) + ".wav"

stream.save_to_wav_file(filename)