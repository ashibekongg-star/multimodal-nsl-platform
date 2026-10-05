from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Optional
)


class UpdateProfileForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    bio = TextAreaField(
        "Bio",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    profile_image = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Images only!"
            )
        ]
    )

    submit = SubmitField(
        "Save Changes"
    )