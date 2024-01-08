from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests
from flask_login import login_required, current_user
from .models import User

API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"

trades = Blueprint('trades', __name__)

@trades.route('/')
@login_required
def lib():
    # get user's books
    user_books = User.query("SELECT * FROM user_books WHERE user_id = %s", (current_user.id,))
    books = []
    for book in user_books:
        books.append(User.query("SELECT * FROM books WHERE book_id = %s", (book[2],))[0])

    return render_template("library.html", books=books)

@trades.route('/search', methods=['GET', 'POST'])
@login_required
def search_book():
    print(request.endpoint)
    if request.method == 'POST':
        search = request.form.get('search')
        data = requests.get(API_BASE_URL + "?q=" + search).json()
        return render_template("search.html", books=data.get('items'), search_query=search)
    return redirect(url_for('trades.lib'))

@trades.route('/add')
@login_required
def add_book():
    book_id = request.args.get('book_id')

    book = requests.get(API_BASE_URL + "/" + book_id).json().get('volumeInfo')
    
    # insert book into database if it doesn't exist
    book_exists = User.query("SELECT * FROM books WHERE book_id = %s", (book_id,))
    if not book_exists:
        User.query("INSERT INTO books (book_id, title, author, description, image_url) VALUES (%s, %s, %s, %s, %s)", (book_id, book.get('title'), book.get('authors')[0] if book.get('authors') else 'Unknown Author', book.get('description'), book.get('imageLinks').get('thumbnail')))
    # insert book into user's library
    User.query("INSERT INTO user_books (user_id, book_id) VALUES (%s, %s)", (current_user.id, book_id))

    flash('Book added to library!', category='success')
    return redirect(url_for('trades.lib'))

@trades.route('/remove')
@login_required
def remove_book():
    book_id = request.args.get('book_id')

    # remove book from user's library
    User.query("DELETE FROM user_books WHERE user_id = %s AND book_id = %s", (current_user.id, book_id))

    flash('Book removed from library!', category='success')
    return redirect(url_for('trades.lib'))
