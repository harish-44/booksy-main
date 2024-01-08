from flask import Blueprint, render_template
from .models import User
import requests

book = Blueprint('book', __name__)

@book.route('/<book_id>')
def book_info(book_id):
    book_owners = User.query("SELECT * FROM user_books WHERE book_id = %s", (book_id,))
    users = []
    for user in book_owners:
        users.append(User.query("SELECT * FROM users WHERE id = %s", (user[1],))[0])
    book_info = requests.get("https://www.googleapis.com/books/v1/volumes/" + book_id).json()
    return render_template("book.html", book_owners=users, book=book_info)

