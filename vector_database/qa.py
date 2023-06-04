# -*- coding: utf-8 -*-
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from config.config import *
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

EMEBEDDING_HUGGINGFACE = 1
EMBEDDING_OPENAI = 0


class QAVector:
    def __init__(self, host='localhost', port='19530', collection_name="", dim=1024, emb_type=EMEBEDDING_HUGGINGFACE):
        self.emb_type = emb_type
        connections.connect(host=host, port=port)
        self.collection_name = collection_name
        self.dim = dim
        self.collection = Collection(self.collection_name)
        self.embeddings = self.get_embedding_func()

    def get_embedding_func(self):
        if self.emb_type == EMEBEDDING_HUGGINGFACE:
            model_kwargs = {'device': EMBEDDING_DEVICE}
            return HuggingFaceEmbeddings(
                model_name="GanymedeNil/text2vec-large-chinese",
                model_kwargs=model_kwargs)
        else:
            return OpenAIEmbeddings()

    def create_collection(self):
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        fields = [
            FieldSchema(name='id', dtype=DataType.INT64,
                        is_primary=True, auto_id=False),
            FieldSchema(name="question", dtype=DataType.VARCHAR,
                        max_length=1024),
            FieldSchema(name="answer", dtype=DataType.VARCHAR,
                        max_length=1024),
            FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR,
                        descrition='embedding vectors', dim=self.dim)
        ]
        schema = CollectionSchema(fields=fields, description="QA collection")
        self.collection = Collection(self.collection_name, schema=schema)

        index_params = {
            'metric_type': 'L2',
            'index_type': "IVF_FLAT",
            'params': {"nlist": 2048}
        }
        self.collection.create_index(
            field_name="embedding", index_params=index_params)

        print(f"Collection {self.collection_name} created successfully!")
        return self.collection

    def insert(self, id, question, answer):
        question_vector = self.embeddings.embed_query(question)

        data = [
            [id],
            [question],
            [answer],
            [question_vector]
        ]
        try:
            self.collection.insert(data)
            self.collection.flush()
            print(
                f"Insert {question} successfully!, collection size is {self.collection.num_entities}")
        except Exception as e:
            print(f"Failed to insert: {e}")

    def delete(self, id):
        self.collection.load()
        try:
            res = self.collection.delete(expr="id in [ " + str(id) + "]")
            print(f"- Deleted entities: {res}")
            self.collection.flush()
        except Exception as e:
            print(f"Failed to delete: {e}")

    def update(self, id, new_question, new_answer):
        # 请注意 Milvus 的更新操作是通过删除旧的实体并插入新的实体来完成的
        self.delete(id)
        return self.insert(id, new_question, new_answer)

    def query(self, question):
        # 将问题转化为向量
        question_vector = self.embeddings.embed_query(question)
        search_params = {"metric_type": "L2",
                         "params": {"nprobe": 10}, "offset": 0}
        self.collection.load()

        results = self.collection.search(
            data=[question_vector],
            anns_field="embedding",
            param=search_params,
            limit=1,
            expr=None,
            # set the names of the fields you want to retrieve from the search result.
            output_fields=['id', "question", "answer"],
            consistency_level="Strong"
        )
        return results


if __name__ == "__main__":
    # 设置集合参数
    dim = 1536  # 假设我们使用 BERT 模型，它的向量维度是 768
    collection_name = 'qa'

    set_env()
    set_openai()

    db = QAVector(host="localhost", port=19530, collection_name=collection_name, dim=dim,
                  emb_type=EMBEDDING_OPENAI)

    # 创建集合
    db.create_collection()

    question = "你是谁"
    answer = "我是兵兵"
    db.insert(1, question, answer)

    question = "hack是什么"
    answer = "hack是一种生活方式"
    db.insert(2, question, answer)

    question = "你喜欢什么"
    answer = "我喜欢吃饭"
    db.insert(3, question, answer)

    # 查询问题 "你是谁" 的答案
    res = db.query("你是谁")
    print(res)

    # 更新数据
    new_question = "你是谁"
    new_answer = "我是大兵"
    db.update(1, new_question, new_answer)

    # 再次查询问题 "你是谁" 的答案
    res = db.query("你是谁")
    print(res)

    # 删除问题 "hack是什么" 的数据
    db.delete(2)
