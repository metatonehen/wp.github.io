import os

from flask import Flask, request, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_babel import Babel


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "metatonehen_secret_key"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# configure the database using DATABASE_URL from environment
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Define locale selector function
def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']
    
    # Or try to guess the language from the user accept header
    supported_locales = ['en', 'es', 'it', 'pt', 'de']
    return request.accept_languages.best_match(supported_locales)

# Configure Babel for translations
babel = Babel(
    app, 
    default_locale='en', 
    default_translation_directories='translations',
    locale_selector=get_locale
)

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()

# Import routes after app and db are created to avoid circular imports
from routes import *