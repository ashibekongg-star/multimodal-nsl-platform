from flask import (
    Blueprint,
    render_template,
    request
)

from app.translator.service import translate_text


translator_bp = Blueprint(
    "translator",
    __name__,
    url_prefix="/translator"
)


@translator_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Text → Nigerian Sign Language Translator
    """

    query = ""
    matched_signs = []
    unknown_words = []

    if request.method == "POST":

        query = request.form.get(
            "text",
            ""
        )

        matched_signs, unknown_words = translate_text(query)

    return render_template(
        "translator/index.html",
        query=query,
        matched_signs=matched_signs,
        unknown_words=unknown_words
    )