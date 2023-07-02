import streamlit as st
import sqlite3
import pandas as pd

def create_table():
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS qa (question TEXT, answer TEXT)")
    conn.commit()
    conn.close()

def add_data(question, answer):
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("INSERT INTO qa (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def view_all_data():
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("SELECT * FROM qa")
    data = c.fetchall()
    conn.close()
    return data

def delete_data(question):
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("DELETE FROM qa WHERE question=?", (question,))
    conn.commit()
    conn.close()

def update_data(question, answer):
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("UPDATE qa SET answer=? WHERE question=?", (answer, question))
    conn.commit()
    conn.close()

def main():
    st.title("Q&A Management")

    menu = ["View all", "Add", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select Menu", menu)

    if choice == "View all":
        st.subheader("View all Q&A")
        result = view_all_data()
        df = pd.DataFrame(result, columns=["Question", "Answer"])
        st.dataframe(df)

    elif choice == "Add":
        st.subheader("Add a new Q&A")
        question = st.text_input("Question")
        answer = st.text_input("Answer")
        if st.button("Add Q&A"):
            add_data(question, answer)
            st.success("Q&A added successfully")

    elif choice == "Update":
        st.subheader("Update Q&A")
        question = st.text_input("Question to Update")
        answer = st.text_input("New Answer")
        if st.button("Update Q&A"):
            update_data(question, answer)
            st.success("Q&A updated successfully")

    elif choice == "Delete":
        st.subheader("Delete Q&A")
        question = st.text_input("Question to Delete")
        if st.button("Delete Q&A"):
            delete_data(question)
            st.success("Q&A deleted successfully")

if __name__ == "__main__":
    create_table()
    main()