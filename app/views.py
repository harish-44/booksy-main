from flask import Blueprint, render_template
from .models import User
from flask_login import current_user, login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
    recent_books = []
    recent_users = User.query("SELECT * FROM user_books ORDER BY id DESC LIMIT 5")
    for user in recent_users:
        book = User.query("SELECT * FROM books WHERE book_id = %s", (user[2],))[0]
        book = book + (User.query("SELECT * FROM users WHERE id = %s", (user[1],))[0][1],)
        recent_books.append(book)

    return render_template("home.html", books=recent_books)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template("settings.html", user=current_user)
