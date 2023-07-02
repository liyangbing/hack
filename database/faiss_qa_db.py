import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class FaissQAIndex:
    def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.data = []

    def add_data(self, data):
        question, answer = data
        for i, (q, a) in enumerate(self.data):
            if q == question:
                self.data[i] = (question, answer)  # 更新答案
                return
        self.data.append(data)  # 问题不存在，添加新数据

    def build_index(self):
        question_vectors = np.array(
            [self.model.encode(question) for question, _ in self.data])
        self.index = faiss.IndexFlatL2(question_vectors.shape[1])
        self.index.add(question_vectors)

    def search(self, input_question, k=1):
        input_question_vector = self.model.encode(input_question)
        input_question_vector = np.array([input_question_vector])
        distances, indices = self.index.search(input_question_vector, k)
        results = []
        for i in range(k):
            result = {
                "question": self.data[indices[0][i]][0],
                "answer": self.data[indices[0][i]][1],
                "distance": distances[0][i]
            }
            results.append(result)
        return results

    def delete_data(self, question):
        self.data = [(q, a) for q, a in self.data if q != question]
        self.build_index()

    def update_data(self, question, new_answer):
        for i, (q, a) in enumerate(self.data):
            if q == question:
                self.data[i] = (question, new_answer)
        self.build_index()

    def search_by_distance(self, input_question, distance_threshold=0.5):
        """
        根据distance阈值检索，调用类方法search, 返回符合条件的1个值
        小于distance_threshold，返回： {"hit": True, "question": "xxx", "answer": "xxx"}
        大于distance_threshold，返回： {"hit": False, "question": “xxx", "answer": "xxx"}
        """
        results = self.search(input_question)
        hit = False
        if results[0]["distance"] < distance_threshold:
            hit = True
        return {"hit": hit, "question": results[0]["question"], "answer": results[0]["answer"], "distance": results[0]["distance"]}
    

            
        

        
        
