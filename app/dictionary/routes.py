from flask import Blueprint, render_template, request

from app.models.category import Category
from app.models.sign import Sign


dictionary_bp = Blueprint(
    "dictionary",
    __name__,
    url_prefix="/dictionary"
)


@dictionary_bp.route("/")
def categories():
    """
    Display all dictionary categories.
    """

    categories = Category.query.order_by(Category.name.asc()).all()

    return render_template(
        "dictionary/categories.html",
        categories=categories
    )


@dictionary_bp.route("/category/<int:category_id>")
def category(category_id):
    """
    Display all signs belonging to one category.
    """

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


@dictionary_bp.route("/sign/<int:sign_id>")
def sign(sign_id):
    """
    Display details of a single sign.
    """

    sign = Sign.query.get_or_404(sign_id)

    return render_template(
        "dictionary/sign.html",
        sign=sign
    )


@dictionary_bp.route("/search")
def search():

    query = request.args.get("q", "").strip()

    signs = []

    if query:

        signs = (
            Sign.query.filter(
                Sign.word.ilike(f"%{query}%")
            )
            .order_by(Sign.word.asc())
            .all()
        )

    return render_template(
        "dictionary/search.html",
        query=query,
        signs=signs
    )