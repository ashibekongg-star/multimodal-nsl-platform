from app import db
from app.models.category import Category

CATEGORIES = [
    {"name": "Greetings", "description": "Greetings and introductions"},
    {"name": "Common Phrases", "description": "Frequently used expressions"},
    {"name": "Alphabet", "description": "A–Z fingerspelling"},
    {"name": "Numbers", "description": "Numbers and counting"},
    {"name": "Family", "description": "Family members and relationships"},
    {"name": "Education", "description": "Schools, teachers, students and learning"},
    {"name": "Food & Drinks", "description": "Food and beverages"},
    {"name": "Animals", "description": "Domestic and wild animals"},
    {"name": "Transportation", "description": "Vehicles and transport"},
    {"name": "Places", "description": "Buildings and locations"},
    {"name": "Health & Medical", "description": "Health and healthcare"},
    {"name": "Emergency & Safety", "description": "Emergency communication"},
    {"name": "Occupations", "description": "Jobs and professions"},
    {"name": "Technology", "description": "Computers and digital technology"},
    {"name": "Religion", "description": "Religious terms"},
    {"name": "Sports", "description": "Sports and games"},
    {"name": "Time & Date", "description": "Time expressions"},
    {"name": "Weather", "description": "Weather conditions"},
    {"name": "Colours", "description": "Colours"},
    {"name": "Clothing", "description": "Clothes and accessories"},
    {"name": "Household Items", "description": "Objects found at home"},
    {"name": "Nature", "description": "Plants and natural environment"},
    {"name": "Body Parts", "description": "Human body"},
    {"name": "Emotions", "description": "Feelings and emotions"},
    {"name": "Communication", "description": "Language and communication"},
    {"name": "Questions", "description": "Question words"},
    {"name": "Actions", "description": "Common verbs"},
    {"name": "Adjectives", "description": "Describing words"},
    {"name": "Business", "description": "Business and commerce"},
    {"name": "Banking & Finance", "description": "Money and banking"},
    {"name": "Government", "description": "Government and politics"},
    {"name": "Agriculture", "description": "Farming"},
    {"name": "Science", "description": "Scientific terms"},
    {"name": "Mathematics", "description": "Mathematics"},
    {"name": "ICT & Computing", "description": "Information Technology"},
    {"name": "Entertainment", "description": "Music, movies and arts"},
    {"name": "Travel & Tourism", "description": "Travel"},
    {"name": "Nigerian Culture", "description": "Culture and traditions"},
    {"name": "Deaf Education", "description": "Deaf education terminology"},
    {"name": "Sign Language Grammar", "description": "Grammar and non-manual features"},
]


def seed_categories():
    added = 0

    for category in CATEGORIES:
        exists = Category.query.filter_by(name=category["name"]).first()

        if exists:
            continue

        db.session.add(Category(**category))
        added += 1

    db.session.commit()

    print(f"Added {added} new categories.")