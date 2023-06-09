import gradio as gr

from conversation.langchain_agent import ask


def chat_interface(question):
    return ask(question)

iface = gr.Interface(
    fn=chat_interface,  # the function to wrap
    inputs=gr.inputs.Textbox(
        lines=2, placeholder="请输入您的问题..."),  # input specification
    outputs="text",  # output specification
)

iface.launch(server_port=8080, ip)
