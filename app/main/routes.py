from flask import Blueprint, render_template

from app.models.sign import Sign
from app.models.category import Category
from app.models.user import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():

    total_signs = Sign.query.count()

    total_categories = Category.query.count()

    total_users = User.query.count()

    total_videos = Sign.query.filter(
        Sign.video_filename.isnot(None)
    ).count()

    return render_template(
        "main/index.html",
        total_signs=total_signs,
        total_categories=total_categories,
        total_users=total_users,
        total_videos=total_videos,
    )