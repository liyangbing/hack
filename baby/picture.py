from database.oss_db import OSSDB
from database.sqllite_db import SQLiteDB
from io import BytesIO
import json
import time
import uuid
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from config.config import logging
import config.config as config
import langchain
from langchain.cache import InMemoryCache
from database.faiss_qa_db import FaissQAIndex
from baby.stable import PicGenerator

sqllite_db = "/opt/hack/dataset/zhibo/db.sqlite3"

temp_file_dir = "/opt/temp/"

distance_threshold = 3


picGenerator = PicGenerator()

ossDB = OSSDB(config.OSS_ACCESS_KEY_ID, config.OSS_ACCESS_KEY_SECRET,
              config.OSS_ENDPOINT, config.OSS_BUCKET, config.OSS_PREFIX)


chat_gpt_question_template = """
    你是一个自然科学家，需要创建一个10页的绘本来解答孩子的问题
    要求如下：
    1、回答要尽可能的全面，从多角度回答
    2、每页需要有一个图像描述和一个相关的文本描述
    3、直接给出json答案,不需要注释或解释
    4、回答例子,要包括不少于10条：
    5、下面是一个答案的例子，答案是一个json数组
    6、回答内容不要有任何多于的解释，仅仅包括json数组，可以python解析

    [
    {{"image": "A dinosaur hatching from an egg.", "text": "这是一个正在孵化的恐龙蛋，恐龙宝宝就要从中破壳而出。你知道吗，恐龙是从蛋中孵化出来的。"}},
    {{"image": "A young dinosaur with its mother.", "text": "这是一只年轻的恐龙和它的妈妈，恐龙妈妈会照顾小恐龙，直到它们能够自己找食物和保护自己。"}},
    {{"image": "A herd of herbivorous dinosaurs eating plants.", "text": "这是一群正在吃植物的草食性恐龙，恐龙可以分为肉食性和草食性两类。"}},
    {{"image": "A T-Rex hunting for food.", "text": "这是一只正在狩猎的霸王龙，霸王龙是最著名的肉食性恐龙，它们是顶级掠食者。"}},
    {{"image": "Dinosaurs living in a forest.", "text": "这是一些生活在森林中的恐龙，恐龙生活的环境非常多样，包括森林、沙漠、沼泽等。"}},
    {{"image": "A flying dinosaur in the sky.", "text": "这是天空中的飞龙，有些恐龙能够飞翔，它们的翅膀其实是进化来的前肢。"}},
    {{"image": "Dinosaurs fleeing from a volcanic eruption.", "text": "这是一些正在从火山爆发中逃离的恐龙，火山爆发和气候变化是恐龙灭绝的原因之一。"}},
    {{"image": "Fossils of dinosaurs in a museum.", "text": "这是博物馆中的恐龙化石，我们通过研究化石来了解恐龙的生活。"}},
    {{"image": "A scientist studying a dinosaur bone.", "text": "这是一位正在研究恐龙骨头的科学家，科学家通过研究恐龙骨骼来了解它们的生理结构。"}},
    {{"image": "Children looking at a dinosaur model in a theme park.", "text": "这是一些在主题公园里看恐龙模型的孩子，虽然恐龙已经灭绝，但我们可以通过模型和电影来感受它们的壮观。"}}
    ]
    下面是问题
    {human_input}
"""


def generate_random_filename():
    # 使用uuid模块生成一个UUID，并去除其中的破折号(-)和大写字母
    random_filename = str(uuid.uuid4()).replace('-', '').lower()
    return random_filename


class Pic():
    def __init__(self, num_of_round=10):
        self.num_of_round = num_of_round
        self.promptTemplate = PromptTemplate(
            input_variables=["human_input"],

            template=chat_gpt_question_template
        )
        langchain.llm_cache = InMemoryCache()
        logging.debug("cache ChatSimpleGPT init")
        self.llm_chain = LLMChain(
            llm=OpenAI(max_tokens=2048),
            prompt=self.promptTemplate,
            verbose=True
        )

        logging.info("init vector store,use db: %s", sqllite_db)
          # 添加数据到向量索引并重新建立索引
        self.db = SQLiteDB(config.sqllite_db)
        self.faiss_index = FaissQAIndex()

        self.faiss = self.build_faiss_index()

      

    def pic(self, question):
        start_time = time.time()
        vector_result = self.faiss.search_by_distance(
            question, distance_threshold)
        logging.info("ChatSimpleGPT ask question %s, distance_threshold: %f, vector_result: %s",
                     question, distance_threshold, vector_result)

        # 根据vector_result hit判断是否命中
        if vector_result["hit"]:
            answer = vector_result["answer"]
        else:
            answer_string = self.llm_chain.predict(human_input=question)

            # 将字符串解析为Python对象
            answer = json.loads(answer_string)
            for item in answer:
                pic_url = self.get_image_url(item["image"])
                item["url"] = pic_url

            answer_string = json.dumps(answer)
            # 添加数据到数据库
            self.db.insert(config.sqllite_db_table, [None, question, answer_string])
            self.faiss_index.add_data((question, answer_string))
            self.faiss_index.build_index()

        end_time = time.time()
        logging.debug("ChatSimpleGPT ask elase time: %s秒, question: %s, answer: %s",
                      end_time - start_time, question, answer)

        return answer

    def get_image_url(self, image_text: str) -> str:
        image = picGenerator.generate(image_text)
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format='PNG')
        oss_file_name = generate_random_filename() + ".png"

        image.save(temp_file_dir + oss_file_name)

        ossDB.upload_file(temp_file_dir + oss_file_name, oss_file_name)

        # to call the real API that generates a picture based on the string.
        return f"https://{config.OSS_BUCKET}.{config.OSS_ENDPOINT}/{config.OSS_PREFIX}{oss_file_name}"

    def build_faiss_index(self):
        faiss_index = FaissQAIndex()
        datas = self.db.select(config.sqllite_db_table, columns='question, answer')
        for data in datas:
            faiss_index.add_data(data)
        faiss_index.build_index()
        return faiss_index
