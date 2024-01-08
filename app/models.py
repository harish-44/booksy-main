from flask_login import UserMixin
import mysql.connector
from .config import db_config

# db = mysql.connector.connect(**db_config)
# cursor = db.cursor()

import psycopg2


db = psycopg2.connect(
    host="dpg-cm4io7vqd2ns73ekh6a0-a.singapore-postgres.render.com",
    database="booksydb",
    user="root",
    password="8GyJIlNQHbtULlJK0T0GYbeBNg2Lh5tI"
)
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY generated always as identity, name VARCHAR(255), email VARCHAR(255) UNIQUE, username VARCHAR(255) UNIQUE, password VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS books (book_id VARCHAR(255) PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), description TEXT, image_url TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS user_books (id INT PRIMARY KEY generated always as identity, user_id INT, book_id VARCHAR(255), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (book_id) REFERENCES books(book_id))")
db.commit()


class User(UserMixin):
    def __init__(self, id, name, email, username, password):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def query(query, params=None):
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        res = []
        if query.split()[0].lower() == 'select':
            res = cursor.fetchall()
        db.commit()
        return res
    
    def get(id):
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        new_user = cursor.fetchone()
        return User(*new_user) if new_user else None
    
    def add(self):
        cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (self.name, self.email, self.username, self.password))
        db.commit()

