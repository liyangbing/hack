
import base64
import time
from speech import Speech
import logging
import websockets, ssl
import json
import traceback
import asyncio

theresult=""
async def speech2text(audio,uri):
      global theresult
      try:
        chunk_size=[5,10,5]
        chunk_interval=10
        start_time = time.time()
        ssl_context = ssl.SSLContext()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        print("uri=",uri)
        async with websockets.connect(uri, subprotocols=["binary"], ping_interval=None, ssl=ssl_context) as websocket:
            
            message = json.dumps({"mode": "offline", "chunk_size":chunk_size , "chunk_interval": chunk_interval,
                              "wav_name": "hack", "is_speaking": True})
            await websocket.send(message)
            audio_bytes = base64.b64decode(audio)
            stride = int(60 * chunk_size[1] / chunk_interval / 1000 * 16000 * 2)
            chunk_num = (len(audio_bytes) - 1) // stride + 1

            is_speaking = True
            
            for i in range(chunk_num):

                beg = i * stride
                data = audio_bytes[beg:beg + stride]
                message = data
 
                await websocket.send(message)
                if i == chunk_num - 1:
                    is_speaking = False
                    message = json.dumps({"is_speaking": is_speaking})
                    print("len data",message)
                    await websocket.send(message)
 
            sleep_duration = 0.0001
            
            await asyncio.sleep(sleep_duration)
 
            meg = await websocket.recv()
 
            meg = json.loads(meg)
            wav_name = meg.get("wav_name", "demo")
            text = meg["text"]
            prompt = text
 
            end_time = time.time()
            logging.debug("SpeechFunasr audio to text, elase time: %s秒, out_file: %s, result: %s,text: %s", end_time - start_time,  meg, prompt)
            
            theresult= prompt
      except Exception as e:
            print("Exception:", e)
class SpeechFunasr(Speech):
    def __init__(self,host,port):
        uri = "wss://{}:{}".format(host, port)
        self.uri=uri
        
        
    def text_2_audio(self, text):
        pass
    def audio_2_text(self, audio):
        global theresult
        asyncio.run(speech2text(audio,self.uri))
        return theresult
        



def testexample():
    speechobj=SpeechFunasr("39.98.181.185",50001)
    import wave
 
    with wave.open("asr_example.wav", "rb") as wav_file:
                params = wav_file.getparams()
                frames = wav_file.readframes(wav_file.getnframes())
                audio_bytes = bytes(frames)
                b64data=base64.b64encode(audio_bytes)
                text=speechobj.audio_2_text(b64data)
                print("text=",theresult)
 
#testexample()

                
