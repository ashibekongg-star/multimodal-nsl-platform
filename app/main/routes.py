from flask import Blueprint

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return """
    <h1>Nigerian Sign Language Communication Platform</h1>
    <p>Your platform is working!</p>
    """