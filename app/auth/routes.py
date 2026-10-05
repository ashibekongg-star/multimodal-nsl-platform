import os
import uuid

from werkzeug.utils import secure_filename

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db, bcrypt
from app.models.user import User

from app.auth.forms import (
    LoginForm,
    RegisterForm,
    UpdateProfileForm
)

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =====================================================
# REGISTER
# =====================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:

            flash(
                "Email address already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(

            full_name=form.full_name.data,

            email=form.email.data,

            password=hashed_password,

            role=form.role.data

        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form
    )


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(
                user,
                remember=True
            )

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(
                url_for("main.home")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )


# =====================================================
# USER PROFILE
# =====================================================

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = UpdateProfileForm()

    if request.method == "GET":

        form.full_name.data = current_user.full_name
        form.phone.data = current_user.phone
        form.bio.data = current_user.bio

    if form.validate_on_submit():

        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.bio = form.bio.data

        if form.profile_image.data:

            image = form.profile_image.data

            filename = secure_filename(
                image.filename
            )

            extension = os.path.splitext(
                filename
            )[1]

            unique_filename = (
                f"{uuid.uuid4().hex}{extension}"
            )

            upload_folder = os.path.join(
                current_app.static_folder,
                "profile_images"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    upload_folder,
                    unique_filename
                )
            )

            current_user.profile_image = unique_filename

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("auth.profile")
        )

    return render_template(
        "auth/profile.html",
        form=form
    )


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have successfully logged out.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )