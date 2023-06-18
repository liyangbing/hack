import streamlit as st

# 示例数据
data = [
    {"id": 1, "question": "问题 1", "answer": "答案 1"},
    {"id": 2, "question": "问题 2", "answer": "答案 2"},
    {"id": 3, "question": "问题 3", "answer": "答案 3"},
]

# 用于向后端发送数据的函数
def send_to_backend(selected_data):
    # 在这里添加将数据发送到后端的逻辑
    st.write(f"发送到后端的数据: {selected_data}")

# 标题
st.title("问题和答案")


# 初始化选中的项目列表
selected_items = []

# 创建表头
header_columns = st.columns(4)
header_columns[0].write("")
header_columns[1].write("ID")
header_columns[2].write("问题")
header_columns[3].write("答案")

# 创建表格，将选择框放在第一列
for item in data:
    columns = st.columns(4)
    is_selected = columns[0].checkbox(f"Select {item['id']}", key=f"checkbox_{item['id']}", value=False, label_visibility='hidden')  # 在这里添加选择框并隐藏标签
    if is_selected:
        selected_items.append(item)
    columns[1].write(item["id"])
    columns[2].write(item["question"])
    columns[3].write(item["answer"])

# 点击按钮后将选中的行发送到后端
if st.button("添加到向量数据库"):
    send_to_backend(selected_items)