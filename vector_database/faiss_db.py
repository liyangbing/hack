import numpy as np
import faiss
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer


# 准备数据集（问题，答案）
data = [
    ("What is the capital of France?", "Paris"),
    ("How many legs does a spider have?", "8"),
    ("What is the color of the sky?", "blue"),
    ("What is the smallest ocean?", "Arctic Ocean")
]

# 使用sentence-transformers库将问题向量化
#model = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

question_vectors = np.array([model.encode(question) for question, _ in data])

# 创建Faiss内存索引
index = faiss.IndexFlatL2(question_vectors.shape[1])
index.add(question_vectors)

# 用户输入的问题
input_question = "Which ocean is the smallest?"

# 将输入问题向量化
input_question_vector = model.encode(input_question)
input_question_vector = np.array([input_question_vector])

# 在Faiss索引中搜索相似问题
k = 1  # 搜索最相似的问题数量
distances, indices = index.search(input_question_vector, k)

# 返回与找到的相似问题关联的答案
for i in range(k):
    print(f"Answer: {data[indices[0][i]][1]} (distance: {distances[0][i]})")