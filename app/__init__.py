from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Connect database
    db.init_app(app)

    # Connect database migration system
    migrate.init_app(app, db)

    # Connect main/home-page routes
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)

    # Connect dictionary routes
    from app.dictionary.routes import dictionary_bp
    app.register_blueprint(dictionary_bp)

    # Load database models
    from app.models.user import User
    from app.models.category import Category
    from app.models.sign import Sign

    return app