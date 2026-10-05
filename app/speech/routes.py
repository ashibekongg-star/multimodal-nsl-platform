from flask import (
    Blueprint,
    render_template,
    request,
    make_response
)

from app.translator.service import translate_text

speech_bp = Blueprint(
    "speech",
    __name__,
    url_prefix="/speech"
)


@speech_bp.route("/", methods=["GET", "POST"])
def index():

    recognized_text = ""

    matched_signs = []

    unknown_words = []

    video_files = []

    if request.method == "POST":

        recognized_text = request.form.get(
            "speech",
            ""
        )

        matched_signs, unknown_words = translate_text(
            recognized_text
        )

        print("===== VIDEO FILES =====")

        for sign in matched_signs:
            print(sign.word, sign.video_filename)

        print("=======================")

        # =========================================
        # DEBUG INFORMATION
        # =========================================

        print("\n===================================")
        print("RECOGNIZED TEXT:")
        print(recognized_text)

        print("\nMATCHED SIGNS:")

        if matched_signs:

            for sign in matched_signs:

                print(f"Word: {sign.word}")
                print(f"Video: {sign.video_filename}")
                print("----------------------")

        else:

            print("No matched signs found.")

        print("\nUNKNOWN WORDS:")

        if unknown_words:

            print(", ".join(unknown_words))

        else:

            print("None")

        print("===================================\n")

        # =========================================
        # Build video queue
        # =========================================

        video_files = [
            sign.video_filename
            for sign in matched_signs
        ]

    # =========================================
    # Render page
    # =========================================

    html = render_template(
        "speech/index.html",
        recognized_text=recognized_text,
        matched_signs=matched_signs,
        unknown_words=unknown_words,
        video_files=video_files
    )

    # =========================================
    # Disable browser caching
    # =========================================

    response = make_response(html)

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response