import os
from uuid import uuid4

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from app import db
from app.profile.forms import UpdateProfileForm


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


# =====================================================
# PROFILE PAGE
# =====================================================

@profile_bp.route("/")
@login_required
def profile():

    return render_template(
        "profile/profile.html",
        user=current_user
    )


# =====================================================
# EDIT PROFILE
# =====================================================

@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = UpdateProfileForm()

    # -----------------------------------------
    # SAVE CHANGES
    # -----------------------------------------

    if form.validate_on_submit():

        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.bio = form.bio.data

        # =====================================
        # Upload Profile Image
        # =====================================

        if form.profile_image.data:

            image = form.profile_image.data

            filename = (
                str(uuid4()) +
                "_" +
                secure_filename(image.filename)
            )

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "profile_images"
            )

            # Create folder automatically
            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

            current_user.profile_image = filename

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("profile.profile")
        )

    # -----------------------------------------
    # LOAD EXISTING USER DATA
    # -----------------------------------------

    if not form.is_submitted():

        form.full_name.data = current_user.full_name
        form.phone.data = current_user.phone
        form.bio.data = current_user.bio

    return render_template(
        "profile/edit_profile.html",
        form=form,
        user=current_user
    )