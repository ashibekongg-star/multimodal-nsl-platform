from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# =====================================================
# Extensions
# =====================================================

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Redirect users to login page if not authenticated

login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "warning"

# =====================================================
# User Loader
# =====================================================

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


# =====================================================
# Create Application
# =====================================================

def create_app():

    app = Flask(__name__)

    # -------------------------------------------------
    # Load Configuration
    # -------------------------------------------------

    import os
    from config import config

    config_name = os.getenv("FLASK_ENV", "default")

    app.config.from_object(config[config_name])

    # -------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------

    # Home
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)

    # Authentication
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Profile
    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)

    # Dictionary
    from app.dictionary.routes import dictionary_bp
    app.register_blueprint(dictionary_bp)

    # Speech
    from app.speech.routes import speech_bp
    app.register_blueprint(speech_bp)

    # Translator
    from app.translator.routes import translator_bp
    app.register_blueprint(translator_bp)

    # Administration
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    # -------------------------------------------------
    # Import Models
    # -------------------------------------------------

    from app.models.user import User
    from app.models.category import Category
    from app.models.sign import Sign

    return app