from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    TextAreaField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


# =====================================================
# Register Form
# =====================================================

class RegisterForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("student", "Student"),
            ("interpreter", "Interpreter")
        ]
    )

    submit = SubmitField("Create Account")


# =====================================================
# Login Form
# =====================================================

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")


# =====================================================
# Update Profile Form
# =====================================================

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
        "Profile Picture"
    )

    submit = SubmitField(
        "Update Profile"
    )