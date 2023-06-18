# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import base64

# 读取图片文件内容
with open('/mnt/data/hack/dataset/tts.mp3', 'rb') as file:
    image_data = file.read()

# 将图片数据转换为 Base64 字符串
base64_string = base64.b64encode(image_data).decode('utf-8')

# 将 Base64 字符串写入文件
with open('image.txt', 'w') as file:
    file.write(base64_string)

print(base64_string)

