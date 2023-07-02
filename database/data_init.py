import json
from datetime import datetime
from sqllite_db import SQLiteDB
from config import config
from database.faiss_qa_db import FaissQAIndex


db = SQLiteDB(config.sqllite_db)

# 创建问答表
db.drop_table('qa')
db.create_table('qa', ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'question TEXT', 'answer TEXT', 'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP','update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP'])

# 读取JSONL文件并插入数据到QA表
with open(config.qa_jsonl, 'r') as f:
    for line in f:
        data = json.loads(line)
        question = data['prompt']
        answer = data['completion']
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_time = create_time
        db.insert('qa', [None, question, answer, create_time, update_time])


# 创建Faiss索引对象
index = FaissQAIndex()

# 从数据库中获取数据
datas = db.select('qa', columns='question, answer')

# 添加数据并构建索引
for data in datas:
    index.add_data(data)

index.build_index()

# 用户输入的问题
input_question = "我想搭建一"

# 在Faiss索引中搜索相似问题
results = index.search(input_question, k=1)

# 输出搜索结果
# 增加判断，distance大于5的不要
for result in results:
    if result['distance'] > 5:
        print("没有找到相似问题")
        break
    print(f"Question: {result['question']}")

    print(f"Answer: {result['answer']} (distance: {result['distance']})")


# 关闭连接
db.close()
