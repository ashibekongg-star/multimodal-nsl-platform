from datetime import datetime, timezone

from app import db


class Sign(db.Model):
    __tablename__ = "signs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    word = db.Column(
        db.String(150),
        nullable=False
    )

    meaning = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    video_filename = db.Column(
        db.String(255)
    )

    example_sentence = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    category = db.relationship(
        "Category",
        back_populates="signs"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Sign {self.word}>"