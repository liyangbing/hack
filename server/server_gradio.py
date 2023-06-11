import glob
import logging
import random
import re
import string
import openai, os, time, requests
import gradio as gr
from gradio import HTML
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
<<<<<<< Updated upstream

openai.api_key = os.environ["OPENAI_API_KEY"]
=======
import whisper
from requests_toolbelt.multipart.encoder import MultipartEncoder


import sys
sys.path.append("../")
from config.config import *
from conversation.chat_chatglm import ask,action

import gradio as gr
import base64
import io
from pydub import AudioSegment
import subprocess
from base64 import b64encode


audio_model = whisper.load_model("small")

def play_base64_audio(base64_audio):
    # 将 base64 编码的音频转换为字节流
    audio_data = base64.b64decode(base64_audio)
    
    # 使用 pydub 将字节流转换为 AudioSegment 对象
    audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")  # 更改 format 参数以匹配实际音频格式

    # 将 AudioSegment 对象转换为 wav 文件的字节流
    wav_buffer = io.BytesIO()
    audio.export(wav_buffer, format="wav")
    wav_buffer.seek(0)

    # 返回 wav 文件的字节流
    return wav_buffer
>>>>>>> Stashed changes

memory = ConversationSummaryBufferMemory(llm=ChatOpenAI(), max_token_limit=2048)
conversation = ConversationChain(
    llm=OpenAI(max_tokens=2048, temperature=0.5), 
    memory=memory,
)

avatar_url = "https://cdn.discordapp.com/attachments/1065596492796153856/1095617463112187984/John_Carmack_Potrait_668a7a8d-1bb0-427d-8655-d32517f6583d.png"

#语音合成 voice vits
def voice_vits2(text, id=133, format="wav", lang="zh", length=1, noise=0.667, noisew=0.8, max=30):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max)
    }
    boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{AUDIO_URL}/voice"

    res = requests.post(url=url, data=m, headers=headers)
    if res.status_code != 200:
        logging.error("voice_vits: %s", res.text)
        return ""
    logging.debug("voice_vits: %s", res.headers)
    fname = re.findall("filename=(.+)", res.headers["Content-Disposition"])[0]
    path = f"{AUDIO_SAVA_PATH}/{fname}"

    with open(path, "wb") as f:
        f.write(res.content)

    logging.debug("voice_vits: %s", path)   

    return path

def get_latest_file(path):
  dir_list = glob.glob(path)
  dir_list.sort(key=lambda x: os.path.getmtime(x))
  return dir_list[-1]

def predict(input, history=[]):
    if input is not None:
        history.append(input)
<<<<<<< Updated upstream
        response = conversation.predict(input=input)    
        video_url = get_mp4_video(input=response, avatar_url=avatar_url)
=======
        response = ask(input)

        play_path = voice_vits2(response)

        # copy play_path文件到/opt/jupyter/RAD-NeRF/data目录
        subprocess.run(["cp", play_path, "/opt/jupyter/RAD-NeRF/data"])
        # 获取文件名
        file_name = play_path.split("/")[-1]

        logging.debug("play_path: %s, file_name: %s", play_path, file_name)


         # python /opt/jupyter/RAD-NeRF/nerf/asr.py --wav data/<name>.wav --save_feats # save to data/<name>_eo.npy
        subprocess.run(["python", "/opt/jupyter/RAD-NeRF/nerf/asr.py", "--wav", "/opt/jupyter/RAD-NeRF/data/" + file_name, "--save_feats"])

        subprocess.run(["python", "/opt/jupyter/RAD-NeRF/test.py", "-O", "--torso", 
                        "--pose", "/opt/jupyter/RAD-NeRF/data/pose.json",
                        "--data_range", "0", "100", 
                        "--ckpt", "/opt/jupyter/RAD-NeRF/pretrained/model.pth", 
                        "--aud", f"/opt/jupyter/RAD-NeRF/data/{file_name[:-4]}_eo.npy", 
                        "--bg_img", f"/opt/jupyter/RAD-NeRF/data/bg.jpg", 
                        "--workspace", "/opt/jupyter/RAD-NeRF/trial"])
        
        Video = get_latest_file(os.path.join('/opt/jupyter/RAD-NeRF/trial', 'results', '*.mp4'))
        Video_aud = Video.replace('.mp4', '_aud.mp4')

        subprocess.run(["ffmpeg", "-y", "-i", Video, "-i", f"/opt/jupyter/RAD-NeRF/data/{file_name}", "-c:v", "copy", "-c:a", "aac", Video_aud])

        video_file = open(Video_aud, "r+b").read()
        video_url = f"data:video/mp4;base64,{b64encode(video_file).decode()}"


>>>>>>> Stashed changes
        video_html = f"""<video width="320" height="240" controls autoplay><source src="{video_url}" type="video/mp4"></video>"""
        history.append(response)
        responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
        return responses, video_html, history
    else:
        video_html = f'<img src="{avatar_url}" width="320" height="240" alt="John Carmack">'
        responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
        return responses, video_html, history
        
        

def transcribe(audio):
    os.rename(audio, audio + '.wav')
    audio_file = open(audio + '.wav', "rb")
<<<<<<< Updated upstream
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt="这是一段简体中文的问题。")
    return transcript['text']    
=======
    
    result = audio_model.transcribe(audio=audio + '.wav',language='zh', prompt="这里是黑客松直播间，你是虚拟数字人思思。请用中文")
    logging.debug("audio to text, out_file:  %s, result: %s,text: %s", audio_file,  result, result["text"])

    prompt = result["text"]
    return prompt  
>>>>>>> Stashed changes

def process_audio(audio, history=[]):
    if audio is not None:
        text = transcribe(audio)
        return predict(text, history)
    else:
        text = None
        return predict(text, history)

with gr.Blocks(css="#chatbot{height:500px} .overflow-y-auto{height:500px}") as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
        
    with gr.Row():
        audio = gr.Audio(source="microphone", type="filepath")

    with gr.Row():
        video = gr.HTML(f'<img src="{avatar_url}" width="320" height="240" alt="John Carmack">', live=False)

    txt.submit(predict, [txt, state], [chatbot, video, state])
    audio.change(process_audio, [audio, state], [chatbot, video, state])
    
<<<<<<< Updated upstream
demo.launch()
=======
demo.launch(server_name="0.0.0.0", server_port=50001)


# 语音合成 voice vits
#
    
>>>>>>> Stashed changes
