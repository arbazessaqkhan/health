import os
import logging
from flask import Flask, request, g, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lifeline-hospital-dev-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///lifeline_hospital.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize Babel for internationalization
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel = Babel(app)

# Set the locale selection function without using decorators
def get_locale():
    # If a user is logged in, use their preferred language
    if 'language' in session:
        return session['language']
    # Otherwise use the best match from the Accept-Language header
    return request.accept_languages.best_match(['en', 'hi', 'ur'])

# Use a direct approach of setting the locale selector function
app.jinja_env.globals['get_locale'] = get_locale

# For each request, set the language
@app.before_request
def before_request():
    g.locale = get_locale()

# Import and register blueprints
with app.app_context():
    from views.home import home_bp
    from views.doctors import doctors_bp
    from views.appointments import appointments_bp
    from views.patients import patients_bp
    from views.services import services_bp
    from views.contact import contact_bp
    from views.auth import auth_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(contact_bp, url_prefix='/contact')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Make sure to import models for table creation
    import models
    
    db.create_all()

# Jinja global variables
@app.context_processor
def utility_processor():
    return {
        'languages': {
            'en': 'English',
            'hi': 'हिन्दी (Hindi)', 
            'ur': 'اردو (Urdu)'
        }
    }

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    return None