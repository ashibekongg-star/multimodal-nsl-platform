from pathlib import Path

ROOT = Path("NSL_Communication_Platform")

FILES = {
    "run.py": '''from app import create_app\n\napp = create_app()\n\nif __name__ == "__main__":\n    app.run(debug=True)\n''',

    "config.py": '''import os\nfrom pathlib import Path\n\nBASE_DIR = Path(__file__).resolve().parent\n\nclass Config:\n    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret")\n    SQLALCHEMY_DATABASE_URI = os.getenv(\n        "DATABASE_URL",\n        f"sqlite:///{BASE_DIR / 'nsl_platform.db'}"\n    )\n    SQLALCHEMY_TRACK_MODIFICATIONS = False\n''',

    "app/__init__.py": '''from flask import Flask\nfrom flask_migrate import Migrate\nfrom flask_sqlalchemy import SQLAlchemy\n\ndb = SQLAlchemy()\nmigrate = Migrate()\n\n\ndef create_app():\n    app = Flask(__name__)\n    app.config.from_object("config.Config")\n\n    db.init_app(app)\n    migrate.init_app(app, db)\n\n    from app.main.routes import main_bp\n    app.register_blueprint(main_bp)\n\n    # Import models so SQLAlchemy/Alembic can discover them.\n    from app.models import user, category, sign\n\n    return app\n''',

    "app/main/__init__.py": '''''',

    "app/main/routes.py": '''from flask import Blueprint, jsonify, render_template\n\nmain_bp = Blueprint("main", __name__)\n\n\n@main_bp.route("/")\ndef home():\n    return render_template("home.html")\n\n\n@main_bp.route("/health")\ndef health():\n    return jsonify({\n        "status": "ok",\n        "service": "NSL Communication Platform"\n    })\n''',

    "app/models/__init__.py": '''from app.models.user import User\nfrom app.models.category import Category\nfrom app.models.sign import Sign\n\n__all__ = ["User", "Category", "Sign"]\n''',

    "app/models/user.py": '''from datetime import datetime, timezone\nfrom app import db\n\n\nclass User(db.Model):\n    __tablename__ = "users"\n\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(80), unique=True, nullable=False, index=True)\n    email = db.Column(db.String(255), unique=True, nullable=False, index=True)\n    password_hash = db.Column(db.String(255), nullable=False)\n    first_name = db.Column(db.String(100))\n    last_name = db.Column(db.String(100))\n    role = db.Column(db.String(20), nullable=False, default="user")\n    is_active = db.Column(db.Boolean, nullable=False, default=True)\n    created_at = db.Column(\n        db.DateTime(timezone=True),\n        nullable=False,\n        default=lambda: datetime.now(timezone.utc),\n    )\n    updated_at = db.Column(\n        db.DateTime(timezone=True),\n        nullable=False,\n        default=lambda: datetime.now(timezone.utc),\n        onupdate=lambda: datetime.now(timezone.utc),\n    )\n\n    def __repr__(self):\n        return f"<User {self.username}>"\n''',

    "app/models/category.py": '''from datetime import datetime, timezone\nfrom app import db\n\n\nclass Category(db.Model):\n    __tablename__ = "categories"\n\n    id = db.Column(db.Integer, primary_key=True)\n    name = db.Column(db.String(100), unique=True, nullable=False, index=True)\n    description = db.Column(db.Text)\n    created_at = db.Column(\n        db.DateTime(timezone=True),\n        nullable=False,\n        default=lambda: datetime.now(timezone.utc),\n    )\n\n    signs = db.relationship("Sign", back_populates="category", lazy=True)\n\n    def __repr__(self):\n        return f"<Category {self.name}>"\n''',

    "app/models/sign.py": '''from datetime import datetime, timezone\nfrom app import db\n\n\nclass Sign(db.Model):\n    __tablename__ = "signs"\n\n    id = db.Column(db.Integer, primary_key=True)\n    word = db.Column(db.String(150), nullable=False, index=True)\n    meaning = db.Column(db.Text)\n    description = db.Column(db.Text)\n    video_filename = db.Column(db.String(255))\n    example_sentence = db.Column(db.Text)\n    status = db.Column(db.String(20), nullable=False, default="active")\n    category_id = db.Column(\n        db.Integer,\n        db.ForeignKey("categories.id"),\n        nullable=True,\n        index=True,\n    )\n    created_at = db.Column(\n        db.DateTime(timezone=True),\n        nullable=False,\n        default=lambda: datetime.now(timezone.utc),\n    )\n    updated_at = db.Column(\n        db.DateTime(timezone=True),\n        nullable=False,\n        default=lambda: datetime.now(timezone.utc),\n        onupdate=lambda: datetime.now(timezone.utc),\n    )\n\n    category = db.relationship("Category", back_populates="signs")\n\n    def __repr__(self):\n        return f"<Sign {self.word}>"\n''',

    "app/templates/home.html": '''<!doctype html>\n<html lang="en">\n<head>\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <title>NSL Communication Platform</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            max-width: 900px;\n            margin: 0 auto;\n            padding: 40px 20px;\n        }\n        .card {\n            border: 1px solid #ddd;\n            border-radius: 12px;\n            padding: 24px;\n            margin-top: 20px;\n        }\n        a { margin-right: 18px; }\n    </style>\n</head>\n<body>\n    <h1>Nigerian Sign Language Communication Platform</h1>\n    <p>Stage 1 foundation is running.</p>\n\n    <div class="card">\n        <h2>Foundation modules</h2>\n        <a href="/health">System Health</a>\n        <span>Authentication — coming next</span>\n        <span>Dictionary — coming next</span>\n        <span>Translation — coming next</span>\n    </div>\n</body>\n</html>\n''',

    "requirements.txt": '''Flask\nFlask-SQLAlchemy\nFlask-Migrate\nFlask-Login\nFlask-WTF\npython-dotenv\nWerkzeug\n''',

    ".env.example": '''SECRET_KEY=replace-with-a-long-random-secret\nDATABASE_URL=sqlite:///nsl_platform.db\n''',

    ".gitignore": '''__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n*.db\ninstance/\n.vscode/\n''',

    "README.md": '''# NSL Communication Platform\n\nProduction-oriented Flask platform for Nigerian Sign Language communication.\n\n## Stage 1\n\nThis stage establishes:\n\n- Flask application factory\n- Modular blueprint structure\n- SQLite development database\n- SQLAlchemy models\n- Flask-Migrate migrations\n- Basic health endpoint\n\n## Run\n\n```powershell\npython -m venv .venv\n.venv\\Scripts\\Activate.ps1\npip install -r requirements.txt\nflask --app run.py db init\nflask --app run.py db migrate -m "Initial NSL platform schema"\nflask --app run.py db upgrade\npython run.py\n```\n''',
}

for relative_path, content in FILES.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"SKIP (already exists): {path}")
        continue
    path.write_text(content, encoding="utf-8")
    print(f"CREATED: {path}")

for folder in [
    "app/auth",
    "app/translation",
    "app/dictionary",
    "app/admin",
    "app/api",
    "app/feedback",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "app/static/videos",
    "tests",
]:
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"READY: {path}")

print("\nStage 1 project foundation created successfully.")
print(f"Project location: {ROOT.resolve()}")
