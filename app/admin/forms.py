from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):

    name = StringField(
        "Category Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    description = TextAreaField(
        "Description"
    )

    submit = SubmitField(
        "Save Category"
    )


class SignForm(FlaskForm):
    
    word = StringField(
        "Word",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    meaning = TextAreaField(
        "Meaning"
    )

    description = TextAreaField(
        "Description"
    )

    example_sentence = TextAreaField(
        "Example Sentence"
    )

    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired()]
    )

    video = FileField(
        "Sign Video",
        validators=[
            FileAllowed(
                ["mp4", "webm", "mov"],
                "Only MP4, WEBM and MOV videos are allowed."
            )
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive")
        ],
        default="active"
    )

    submit = SubmitField(
        "Save Sign"
    )

# =====================================================
# USER FORM
# =====================================================

class UserForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            Length(max=30)
        ]
    )

    role = SelectField(
        "Account Role",
        choices=[
            ("student", "Student"),
            ("interpreter", "Interpreter"),
            ("Administrator", "Administrator")
        ],
        validators=[
            DataRequired()
        ]
    )

    bio = TextAreaField(
        "Biography",
        validators=[
            Length(max=500)
        ]
    )

    profile_image = FileField(
        "Profile Photo",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )
        ]
    )

    submit = SubmitField(
        "Save Changes"
    )

    