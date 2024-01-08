from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query("SELECT * FROM users WHERE email = %s", (email,))
        if user:
            user = User(*user[0])
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(request.referrer)

@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 4:
            flash('Password must be greater than 4 characters.', category='error')
        else:
            new_user = User(None, name, email, username, generate_password_hash(password))
            new_user.add()
            user = User.query("SELECT * FROM users WHERE username = %s", (username,))
            login_user(User(*user[0]), remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')