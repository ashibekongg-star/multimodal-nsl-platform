from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # USER INFORMATION
    # =====================================================

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    profile_image = db.Column(
        db.String(255),
        default="default.png",
        nullable=True
    )

    # =====================================================
    # LOGIN INFORMATION
    # =====================================================

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # =====================================================
    # USER ROLE
    # =====================================================

    role = db.Column(
        db.String(50),
        nullable=False,
        default="user"
    )

    # =====================================================
    # ACCOUNT STATUS
    # =====================================================

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    # =====================================================
    # ACCOUNT CREATION DATE
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self):

        return f"<User {self.email}>"