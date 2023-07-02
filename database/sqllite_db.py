import sqlite3
from config import config

class SQLiteDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def drop_table(self, table_name):
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(drop_table_sql)
        self.conn.commit()
        

    def insert(self, table_name, values):
        placeholders = ', '.join(['?' for _ in range(len(values))])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_sql, tuple(values))
        self.conn.commit()

    def update(self, table_name, column, value, condition):
        update_sql = f"UPDATE {table_name} SET {column}=? WHERE {condition}"
        self.cursor.execute(update_sql, (value,))
        self.conn.commit()

    def delete(self, table_name, condition):
        delete_sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(delete_sql)
        self.conn.commit()

    def select(self, table_name, columns='*', condition=None):
        select_sql = f"SELECT {columns} FROM {table_name}"
        if condition:
            select_sql += f" WHERE {condition}"
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()

    def get_all_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# 示例用法
if __name__ == "__main__":
    db = SQLiteDB(config.sqllite_db)

    # 创建问答表
    db.create_table('qa', ['id INTEGER PRIMARY KEY', 'question TEXT', 'answer TEXT', 'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP','update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP'])

    # 遍历所有表
    result = db.get_all_tables()
    for table in result:
        print(table[0])

    db.close()
