from flask import Blueprint, render_template, request, jsonify

from app.models.category import Category
from app.models.sign import Sign


dictionary_bp = Blueprint(
    "dictionary",
    __name__,
    url_prefix="/dictionary"
)


# ==========================================
# Dictionary Home
# ==========================================

@dictionary_bp.route("/")
def categories():

    categories = (
        Category.query
        .order_by(Category.name.asc())
        .all()
    )

    total_signs = Sign.query.count()

    return render_template(
        "dictionary/categories.html",
        categories=categories,
        total_signs=total_signs
    )


# ==========================================
# Category Page
# ==========================================

@dictionary_bp.route("/category/<int:category_id>")
def category(category_id):

    category = Category.query.get_or_404(category_id)

    signs = (
        Sign.query
        .filter_by(category_id=category.id)
        .order_by(Sign.word.asc())
        .all()
    )

    return render_template(
        "dictionary/category.html",
        category=category,
        signs=signs
    )


# ==========================================
# Sign Details
# ==========================================

@dictionary_bp.route("/sign/<int:sign_id>")
def sign(sign_id):

    sign = Sign.query.get_or_404(sign_id)

    related_signs = (
        Sign.query
        .filter(
            Sign.category_id == sign.category_id,
            Sign.id != sign.id,
            Sign.status == "active"
        )
        .order_by(Sign.word.asc())
        .limit(6)
        .all()
    )

    return render_template(
        "dictionary/sign.html",
        sign=sign,
        related_signs=related_signs
    )


# ==========================================
# Search Page
# ==========================================

@dictionary_bp.route("/search")
def search():

    query = request.args.get("q", "").strip()

    signs = []

    if query:

        signs = (
            Sign.query
            .filter(Sign.word.ilike(f"%{query}%"))
            .order_by(Sign.word.asc())
            .all()
        )

    return render_template(
        "dictionary/search.html",
        query=query,
        signs=signs
    )


# ==========================================
# Live Search API
# ==========================================

@dictionary_bp.route("/live-search")
def live_search():

    query = request.args.get("q", "").strip()

    if not query:

        return jsonify([])

    signs = (
        Sign.query
        .filter(Sign.word.ilike(f"%{query}%"))
        .order_by(Sign.word.asc())
        .limit(8)
        .all()
    )

    return jsonify(
        [
            {
                "id": sign.id,
                "word": sign.word,
                "meaning": sign.meaning or ""
            }
            for sign in signs
        ]
    )