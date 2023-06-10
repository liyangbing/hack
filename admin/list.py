import gradio as gr
import time
import requests
import threading

# 用于存储列表数据的变量
data = [{"question": "Question 1", "answer": "Answer 1"},
        {"question": "Question 2", "answer": "Answer 2"}]

def update_data():
    # 这是一个模拟数据更新的函数
    global data
    while True:
        time.sleep(2)  # 每两秒更新一次
        # 请求后端获取新的数据
        res = requests.get("http://localhost:5000/data")
        if res.status_code == 200:
            data = res.json()

def send_to_backend(index):
    # 将数据发送到后端的函数
    requests.post("http://localhost:5000/update", json=data[index])
    return "Updated!"

# 使用线程更新数据
threading.Thread(target=update_data, daemon=True).start()

def gui_fn():
    with gr.Interface(layout="vertical") as gui:
        for i, row in enumerate(data):
            gr.Textbox(readonly=True, value=row["question"])
            gr.Textbox(readonly=True, value=row["answer"])
            gr.Button("Update", on_click=send_to_backend, inputs=[i])
    return gui

gui = gui_fn()
gui.launch()
