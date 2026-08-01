from app import db
from app.models.sign import Sign
from app.models.category import Category

SIGNS = [
    {
        "word": "Hello",
        "category": "Greetings",
        "meaning": "A greeting used when meeting someone.",
        "description": "Common greeting.",
        "video_filename": "hello.mp4",
        "example_sentence": "Hello everyone.",
        "status": "active",
    },
    {
        "word": "Teacher",
        "category": "Education",
        "meaning": "A person who teaches.",
        "description": "Educational term.",
        "video_filename": "teacher.mp4",
        "example_sentence": "The teacher is in the classroom.",
        "status": "active",
    },
]
def seed_signs():
    added = 0

    for sign_data in SIGNS:

        # Check if the sign already exists
        exists = Sign.query.filter_by(
            word=sign_data["word"]
        ).first()

        if exists:
            continue

        # Find the category
        category = Category.query.filter_by(
            name=sign_data["category"]
        ).first()

        if not category:
            print(f"Category '{sign_data['category']}' not found.")
            continue

        # Create the sign
        sign = Sign(
            word=sign_data["word"],
            meaning=sign_data["meaning"],
            description=sign_data["description"],
            video_filename=sign_data["video_filename"],
            example_sentence=sign_data["example_sentence"],
            status=sign_data["status"],
            category_id=category.id
        )

        db.session.add(sign)
        added += 1

    db.session.commit()

    print(f"Added {added} new signs.")