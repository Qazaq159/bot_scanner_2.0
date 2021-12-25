import sqlite3
import os


class DB:
    def __init__(self, db_name):
        conn = sqlite3.connect(os.path.join('db', db_name), check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class DataModel:
    def __init__(self, connection):
        self.connection = connection

    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute('''DROP TABLE products''')
        cursor.close()
        self.connection.commit()

    def check_link(self, link, chat_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE chat_id = ? and link = ?''', (chat_id, link))
        res = cursor.fetchone()
        cursor.close()
        self.connection.commit()

        if res:
            return True
        else:
            return False

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                            (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            link VARCHAR(255),
                            chat_id VARCHAR(255)
                            )
                       ''')
        cursor.close()
        self.connection.commit()

    def insert_product(self, link, chat_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products(link, chat_id)
                          VALUES(?, ?);''', (link, chat_id))
        cursor.close()
        self.connection.commit()

    def get_data(self, chat_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM products WHERE chat_id=?''', (chat_id,))
        res = cursor.fetchall()
        cursor.close()
        self.connection.commit()
        return res
