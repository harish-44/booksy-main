from flask import Flask, render_template, abort
from flask_login import LoginManager
from .models import User
from .config import AppConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    from .auth import auth
    from .views import views
    from .trades import trades
    from .book import book

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(trades, url_prefix='/library')
    app.register_blueprint(book, url_prefix='/book')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"
    login_manager.login_message = "You need to be logged in to access this page."

    @login_manager.user_loader
    def load_user(id):
        return User.get(id)

    return app

def create_db():
    pass
