import streamlit as st
import pandas as pd
from config import config
from database.sqllite_db import SQLiteDB
from database.faiss_qa_db import FaissQAIndex
import logging

class QAApp:
    def __init__(self):
        #打印日志，初始化数据库
        logging.info("init qa app, database info: %s", config.sqllite_db)
        self.db = SQLiteDB(config.sqllite_db)
        self.faiss = self.build_faiss_index()

    def build_faiss_index(self):
        faiss_index = FaissQAIndex()
        datas = self.db.select('qa', columns='question, answer')
        for data in datas:
            faiss_index.add_data(data)
        faiss_index.build_index()
        return faiss_index

    def add(self, question, answer):
        self.db.insert('qa', (None, question, answer, None, None))

    def view_all(self):
        return self.db.select('qa')

    def delete(self, question):
        self.db.delete('qa', f"question='{question}'")

    def update(self, question, answer):
        self.db.update('qa', 'answer', answer, f"question='{question}'")

    def rebuild_index(self):
        self.faiss = self.build_faiss_index()

    def search_vector(self, text):
        return self.faiss.search(text)

    def main(self):
        st.title("Q&A Management")

        menu = ["View all", "Add", "Update", "Delete",
                "Rebuild index", "Vector Search"]
        choice = st.sidebar.selectbox("Select Menu", menu)

        if choice == "View all":
            st.subheader("View all Q&A")
            result = self.view_all()
            df = pd.DataFrame(
                result, columns=["ID", "Question", "Answer", "Create Time", "Update Time"])
            st.dataframe(df)

        elif choice == "Add":
            st.subheader("Add a new Q&A")
            question = st.text_input("Question")
            answer = st.text_input("Answer")
            if st.button("Add Q&A"):
                self.add(question, answer)
                st.success("Q&A added successfully")

        elif choice == "Update":
            st.subheader("Update Q&A")
            question = st.text_input("Question to Update")
            answer = st.text_input("New Answer")
            if st.button("Update Q&A"):
                self.update(question, answer)
                st.success("Q&A updated successfully")

        elif choice == "Delete":
            st.subheader("Delete Q&A")
            question = st.text_input("Question to Delete")
            if st.button("Delete Q&A"):
                self.delete(question)
                st.success("Q&A deleted successfully")
        elif choice == "Rebuild index":
            st.subheader("Rebuild index")
            if st.button("Rebuild index"):
                self.rebuild_index()
                st.success("Index rebuilt successfully")

        elif choice == "Vector Search":
            st.subheader("Vector Search")
            text = st.text_input("Enter text")
            if st.button("Search"):
                result = self.search_vector(text)
                # result是一个list，每个元素是一个dict
                # dict的key有question, answer, distance
                # 遍历输出
                for i, r in enumerate(result):
                    st.write(f"Result {i+1}")
                    st.write(f"Question: {r['question']}")
                    st.write(f"Answer: {r['answer']}")
                    st.write(f"Distance: {r['distance']}")
if __name__ == "__main__":
    app = QAApp()
    app.main()