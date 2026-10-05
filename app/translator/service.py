import re
from app.models.sign import Sign


def translate_text(text):
    """
    Translate English text into Nigerian Sign Language
    while preserving sentence order.
    """

    matched_signs = []
    unknown_words = []

    if not text:
        return matched_signs, unknown_words

    # ----------------------------
    # Clean text
    # ----------------------------

    clean_text = text.lower().strip()
    clean_text = re.sub(r"[^\w\s]", "", clean_text)

    print("\n==============================")
    print("INPUT:", clean_text)

    # ----------------------------
    # Load all signs
    # ----------------------------

    signs = Sign.query.all()

    sign_dict = {
        sign.word.lower(): sign
        for sign in signs
    }

    # ----------------------------
    # Split sentence into words
    # ----------------------------

    words = clean_text.split()

    i = 0

    while i < len(words):

        matched = False

        # Try 3-word phrase
        if i + 2 < len(words):

            phrase = " ".join(words[i:i+3])

            if phrase in sign_dict:

                matched_signs.append(sign_dict[phrase])

                print("Matched:", phrase)

                i += 3

                matched = True

        # Try 2-word phrase
        if not matched and i + 1 < len(words):

            phrase = " ".join(words[i:i+2])

            if phrase in sign_dict:

                matched_signs.append(sign_dict[phrase])

                print("Matched:", phrase)

                i += 2

                matched = True

        # Try single word
        if not matched:

            word = words[i]

            if word in sign_dict:

                matched_signs.append(sign_dict[word])

                print("Matched:", word)

            else:

                unknown_words.append(word)

            i += 1

    print("Unknown:", unknown_words)

    return matched_signs, unknown_words