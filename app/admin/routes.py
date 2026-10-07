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
    login_required,
    current_user
)

from app import db, bcrypt

from app.decorators import admin_required

from app.models.category import Category
from app.models.sign import Sign
from app.models.user import User

from app.admin.forms import (
    CategoryForm,
    SignForm,
    UserForm
)


# =====================================================
# ADMIN BLUEPRINT
# =====================================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =====================================================
# DASHBOARD
# =====================================================

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    # =================================================
    # CATEGORY STATISTICS
    # =================================================

    total_categories = Category.query.count()


    # =================================================
    # SIGN STATISTICS
    # =================================================

    total_signs = Sign.query.count()

    active_signs = Sign.query.filter_by(
        status="active"
    ).count()

    inactive_signs = Sign.query.filter_by(
        status="inactive"
    ).count()


    # =================================================
    # VIDEO STATISTICS
    # =================================================

    total_videos = Sign.query.filter(
        Sign.video_filename.isnot(None)
    ).count()

    active_videos = Sign.query.filter(
        Sign.video_filename.isnot(None),
        Sign.status == "active"
    ).count()

    inactive_videos = Sign.query.filter(
        Sign.video_filename.isnot(None),
        Sign.status == "inactive"
    ).count()


    # =================================================
    # USER STATISTICS
    # =================================================

    total_users = User.query.count()

    active_users = User.query.filter_by(
        status="active"
    ).count()

    inactive_users = User.query.filter_by(
        status="inactive"
    ).count()

    students = User.query.filter_by(
        role="student"
    ).count()

    interpreters = User.query.filter_by(
        role="interpreter"
    ).count()

    administrators = User.query.filter_by(
        role="Administrator"
    ).count()


    # =================================================
    # RECENT SIGNS
    # =================================================

    recent_signs = Sign.query.order_by(
        Sign.created_at.desc()
    ).limit(5).all()


    # =================================================
    # RENDER DASHBOARD
    # =================================================

    return render_template(
        "admin/dashboard.html",

        # Categories
        total_categories=total_categories,

        # Signs
        total_signs=total_signs,
        active_signs=active_signs,
        inactive_signs=inactive_signs,

        # Videos
        total_videos=total_videos,
        active_videos=active_videos,
        inactive_videos=inactive_videos,

        # Users
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        students=students,
        interpreters=interpreters,
        administrators=administrators,

        # Recent signs
        recent_signs=recent_signs
    )


# =====================================================
# CATEGORY MANAGEMENT
# =====================================================

@admin_bp.route("/categories")
@login_required
@admin_required
def categories():

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "admin/categories.html",
        categories=categories
    )


# =====================================================
# ADD CATEGORY
# =====================================================

@admin_bp.route(
    "/categories/add",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def add_category():

    form = CategoryForm()

    if form.validate_on_submit():

        existing_category = Category.query.filter_by(
            name=form.name.data
        ).first()

        if existing_category:

            flash(
                "Category already exists.",
                "warning"
            )

            return render_template(
                "admin/add_category.html",
                form=form
            )

        category = Category(
            name=form.name.data,
            description=form.description.data
        )

        db.session.add(category)

        db.session.commit()

        flash(
            "Category added successfully.",
            "success"
        )

        return redirect(
            url_for("admin.categories")
        )

    return render_template(
        "admin/add_category.html",
        form=form
    )


# =====================================================
# EDIT CATEGORY
# =====================================================

@admin_bp.route(
    "/categories/edit/<int:category_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_category(category_id):

    category = Category.query.get_or_404(
        category_id
    )

    form = CategoryForm(
        obj=category
    )

    if form.validate_on_submit():

        existing_category = Category.query.filter(
            Category.name == form.name.data,
            Category.id != category.id
        ).first()

        if existing_category:

            flash(
                "Category already exists.",
                "warning"
            )

            return render_template(
                "admin/edit_category.html",
                form=form,
                category=category
            )

        category.name = form.name.data

        category.description = (
            form.description.data
        )

        db.session.commit()

        flash(
            "Category updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.categories")
        )

    return render_template(
        "admin/edit_category.html",
        form=form,
        category=category
    )


# =====================================================
# DELETE CATEGORY
# =====================================================

@admin_bp.route(
    "/categories/delete/<int:category_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def delete_category(category_id):

    category = Category.query.get_or_404(
        category_id
    )

    if request.method == "POST":

        if category.signs:

            flash(
                "Cannot delete this category because it contains signs.",
                "danger"
            )

            return redirect(
                url_for("admin.categories")
            )

        db.session.delete(category)

        db.session.commit()

        flash(
            "Category deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin.categories")
        )

    return render_template(
        "admin/delete_category.html",
        category=category
    )


# =====================================================
# SIGN MANAGEMENT
# =====================================================

@admin_bp.route("/signs")
@login_required
@admin_required
def signs():

    search = request.args.get(
        "search",
        ""
    ).strip()

    category_id = request.args.get(
        "category",
        type=int
    )

    status = request.args.get(
        "status",
        ""
    )

    query = Sign.query

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    if search:

        query = query.filter(
            Sign.word.ilike(
                f"%{search}%"
            )
        )

    # -------------------------------------------------
    # CATEGORY FILTER
    # -------------------------------------------------

    if category_id:

        query = query.filter(
            Sign.category_id == category_id
        )

    # -------------------------------------------------
    # STATUS FILTER
    # -------------------------------------------------

    if status:

        query = query.filter(
            Sign.status == status
        )

    signs = query.order_by(
        Sign.word.asc()
    ).all()

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "admin/signs.html",
        signs=signs,
        categories=categories,
        search=search,
        category_id=category_id,
        status=status
    )


# =====================================================
# ADD SIGN
# =====================================================

@admin_bp.route(
    "/signs/add",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def add_sign():

    form = SignForm()

    form.category_id.choices = [
        (
            category.id,
            category.name
        )

        for category in Category.query.order_by(
            Category.name
        ).all()
    ]

    if form.validate_on_submit():

        video_filename = None

        # ---------------------------------------------
        # VIDEO UPLOAD
        # ---------------------------------------------

        if form.video.data:

            video = form.video.data

            filename = secure_filename(
                video.filename
            )

            extension = os.path.splitext(
                filename
            )[1]

            unique_filename = (
                f"{uuid.uuid4().hex}"
                f"{extension}"
            )

            upload_folder = current_app.config[
                "UPLOAD_FOLDER"
            ]

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                upload_folder,
                unique_filename
            )

            video.save(
                save_path
            )

            video_filename = (
                unique_filename
            )

        # ---------------------------------------------
        # CREATE SIGN
        # ---------------------------------------------

        sign = Sign(

            word=form.word.data,

            meaning=form.meaning.data,

            description=form.description.data,

            example_sentence=(
                form.example_sentence.data
            ),

            category_id=form.category_id.data,

            status=form.status.data,

            video_filename=video_filename
        )

        db.session.add(sign)

        db.session.commit()

        flash(
            "Sign added successfully.",
            "success"
        )

        return redirect(
            url_for("admin.signs")
        )

    return render_template(
        "admin/add_sign.html",
        form=form
    )


# =====================================================
# EDIT SIGN
# =====================================================

@admin_bp.route(
    "/signs/edit/<int:sign_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_sign(sign_id):

    sign = Sign.query.get_or_404(
        sign_id
    )

    form = SignForm(
        obj=sign
    )

    form.category_id.choices = [
        (
            category.id,
            category.name
        )

        for category in Category.query.order_by(
            Category.name
        ).all()
    ]

    if form.validate_on_submit():

        sign.word = form.word.data

        sign.meaning = form.meaning.data

        sign.description = (
            form.description.data
        )

        sign.example_sentence = (
            form.example_sentence.data
        )

        sign.category_id = (
            form.category_id.data
        )

        sign.status = (
            form.status.data
        )

        # ---------------------------------------------
        # REPLACE VIDEO
        # ---------------------------------------------

        if form.video.data:

            video = form.video.data

            filename = secure_filename(
                video.filename
            )

            extension = os.path.splitext(
                filename
            )[1]

            unique_filename = (
                f"{uuid.uuid4().hex}"
                f"{extension}"
            )

            upload_folder = current_app.config[
                "UPLOAD_FOLDER"
            ]

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                upload_folder,
                unique_filename
            )

            video.save(
                save_path
            )

            # -----------------------------------------
            # DELETE OLD VIDEO
            # -----------------------------------------

            if sign.video_filename:

                old_video_path = os.path.join(
                    current_app.config[
                        "UPLOAD_FOLDER"
                    ],
                    sign.video_filename
                )

                if os.path.exists(
                    old_video_path
                ):

                    os.remove(
                        old_video_path
                    )

            sign.video_filename = (
                unique_filename
            )

        db.session.commit()

        flash(
            "Sign updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.signs")
        )

    return render_template(
        "admin/edit_sign.html",
        form=form,
        sign=sign
    )


# =====================================================
# VIEW SIGN
# =====================================================

@admin_bp.route(
    "/signs/view/<int:sign_id>"
)
@login_required
@admin_required
def view_sign(sign_id):

    sign = Sign.query.get_or_404(
        sign_id
    )

    return render_template(
        "admin/view_sign.html",
        sign=sign
    )


# =====================================================
# DELETE SIGN
# =====================================================

@admin_bp.route(
    "/signs/delete/<int:sign_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def delete_sign(sign_id):

    sign = Sign.query.get_or_404(
        sign_id
    )

    if request.method == "POST":

        # ---------------------------------------------
        # DELETE VIDEO FILE
        # ---------------------------------------------

        if sign.video_filename:

            video_path = os.path.join(
                current_app.config[
                    "UPLOAD_FOLDER"
                ],
                sign.video_filename
            )

            if os.path.exists(
                video_path
            ):

                os.remove(
                    video_path
                )

        # ---------------------------------------------
        # DELETE DATABASE RECORD
        # ---------------------------------------------

        db.session.delete(
            sign
        )

        db.session.commit()

        flash(
            "Sign deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin.signs")
        )

    return render_template(
        "admin/delete_sign.html",
        sign=sign
    )


# =====================================================
# VIDEO MANAGEMENT
# =====================================================

@admin_bp.route("/videos")
@login_required
@admin_required
def videos():

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()


    # -------------------------------------------------
    # STATUS FILTER
    # -------------------------------------------------

    status_filter = request.args.get(
        "status",
        ""
    ).strip()


    # -------------------------------------------------
    # OVERALL VIDEO STATISTICS
    # These are NOT affected by search/filter.
    # -------------------------------------------------

    total_videos = Sign.query.filter(
        Sign.video_filename.isnot(None)
    ).count()


    active_videos = Sign.query.filter(
        Sign.video_filename.isnot(None),
        Sign.status == "active"
    ).count()


    inactive_videos = Sign.query.filter(
        Sign.video_filename.isnot(None),
        Sign.status == "inactive"
    ).count()


    # -------------------------------------------------
    # VIDEO QUERY
    # -------------------------------------------------

    query = Sign.query.filter(
        Sign.video_filename.isnot(None)
    )


    # -------------------------------------------------
    # SEARCH VIDEOS BY SIGN WORD
    # -------------------------------------------------

    if search:

        query = query.filter(
            Sign.word.ilike(
                f"%{search}%"
            )
        )


    # -------------------------------------------------
    # FILTER VIDEOS BY STATUS
    # -------------------------------------------------

    if status_filter in [
        "active",
        "inactive"
    ]:

        query = query.filter(
            Sign.status == status_filter
        )


    # -------------------------------------------------
    # GET FILTERED VIDEOS
    # -------------------------------------------------

    videos = query.order_by(
        Sign.word.asc()
    ).all()


    # -------------------------------------------------
    # RENDER PAGE
    # -------------------------------------------------

    return render_template(
        "admin/videos.html",

        videos=videos,

        search=search,

        status_filter=status_filter,

        total_videos=total_videos,

        active_videos=active_videos,

        inactive_videos=inactive_videos
    )


# =====================================================
# DELETE VIDEO ONLY
# =====================================================

@admin_bp.route(
    "/videos/delete/<int:sign_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def delete_video(sign_id):

    sign = Sign.query.get_or_404(
        sign_id
    )

    if request.method == "POST":

        if sign.video_filename:

            video_path = os.path.join(
                current_app.config[
                    "UPLOAD_FOLDER"
                ],
                sign.video_filename
            )

            if os.path.exists(
                video_path
            ):

                os.remove(
                    video_path
                )

            sign.video_filename = None

            db.session.commit()

            flash(
                f"Video for '{sign.word}' deleted successfully.",
                "success"
            )

        else:

            flash(
                "This sign does not have a video.",
                "warning"
            )

        return redirect(
            url_for("admin.videos")
        )

    return render_template(
        "admin/delete_video.html",
        sign=sign
    )


# =====================================================
# USER MANAGEMENT
# =====================================================


# =====================================================
# ADD USER
# =====================================================

@admin_bp.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def add_user():

    form = UserForm()

    if form.validate_on_submit():

        # ---------------------------------------------
        # NORMALIZE EMAIL
        # ---------------------------------------------

        email = form.email.data.strip().lower()


        # ---------------------------------------------
        # CHECK FOR EXISTING EMAIL
        # ---------------------------------------------

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "A user with this email address already exists.",
                "warning"
            )

            return render_template(
                "admin/add_user.html",
                form=form
            )


        # ---------------------------------------------
        # PROFILE IMAGE
        # ---------------------------------------------

        profile_image = "default.png"

        image = form.profile_image.data

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            extension = os.path.splitext(
                filename
            )[1].lower()

            unique_filename = (
                f"{uuid.uuid4().hex}"
                f"{extension}"
            )

            upload_folder = current_app.config[
                "PROFILE_IMAGE_FOLDER"
            ]

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                upload_folder,
                unique_filename
            )

            image.save(
                save_path
            )

            profile_image = unique_filename


        # ---------------------------------------------
        # HASH PASSWORD
        # ---------------------------------------------

        hashed_password = (
            bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")
        )


        # ---------------------------------------------
        # CREATE USER
        # ---------------------------------------------

        user = User(

            full_name=form.full_name.data.strip(),

            email=email,

            phone=(
                form.phone.data.strip()
                if form.phone.data
                else None
            ),

            password=hashed_password,

            role=form.role.data,

            bio=(
                form.bio.data.strip()
                if form.bio.data
                else None
            ),

            profile_image=profile_image,

            status="active"
        )


        # ---------------------------------------------
        # SAVE USER
        # ---------------------------------------------

        try:

            db.session.add(user)

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            # -----------------------------------------
            # REMOVE UPLOADED IMAGE IF SAVE FAILED
            # -----------------------------------------

            if profile_image != "default.png":

                uploaded_file = os.path.join(
                    current_app.config[
                        "PROFILE_IMAGE_FOLDER"
                    ],
                    profile_image
                )

                if os.path.exists(
                    uploaded_file
                ):

                    os.remove(
                        uploaded_file
                    )

            current_app.logger.exception(
                "Error creating user: %s",
                error
            )

            flash(
                "Unable to create the user. "
                "Please try again.",
                "danger"
            )

            return render_template(
                "admin/add_user.html",
                form=form
            )


        # ---------------------------------------------
        # SUCCESS MESSAGE
        # ---------------------------------------------

        flash(
            f"User '{user.full_name}' created successfully.",
            "success"
        )


        # ---------------------------------------------
        # REDIRECT
        # ---------------------------------------------

        return redirect(
            url_for(
                "admin.view_user",
                user_id=user.id
            )
        )


    # ---------------------------------------------
    # DISPLAY FORM
    # ---------------------------------------------

    return render_template(
        "admin/add_user.html",
        form=form
    )


# =====================================================
# LIST USERS
# =====================================================

@admin_bp.route("/users")
@login_required
@admin_required
def users():

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )


# =====================================================
# VIEW USER
# =====================================================

@admin_bp.route(
    "/users/view/<int:user_id>"
)
@login_required
@admin_required
def view_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    return render_template(
        "admin/view_user.html",
        user=user
    )


# =====================================================
# EDIT USER
# =====================================================

@admin_bp.route(
    "/users/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(
        user_id
    )


    # ---------------------------------------------
    # FORM
    # ---------------------------------------------

    if request.method == "POST":

        form = UserForm()

    else:

        form = UserForm(
            obj=user
        )


    # ---------------------------------------------
    # IMPORTANT:
    # PASSWORD IS NOT CHANGED HERE
    #
    # The UserForm requires a password for creating
    # a new user. Existing users should not have to
    # enter a new password every time they edit
    # their profile.
    #
    # Therefore, remove the password requirement
    # when editing an existing user.
    # ---------------------------------------------

    form.password.validators = []


    # ---------------------------------------------
    # VALIDATE FORM
    # ---------------------------------------------

    if form.validate_on_submit():

        # -----------------------------------------
        # CHECK DUPLICATE EMAIL
        # -----------------------------------------

        email = form.email.data.strip().lower()

        existing_user = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_user:

            flash(
                "Another user already uses this email address.",
                "warning"
            )

            return render_template(
                "admin/edit_user.html",
                form=form,
                user=user
            )


        # -----------------------------------------
        # UPDATE BASIC INFORMATION
        # -----------------------------------------

        user.full_name = (
            form.full_name.data.strip()
        )

        user.email = email

        user.phone = (
            form.phone.data.strip()
            if form.phone.data
            else None
        )

        user.bio = (
            form.bio.data.strip()
            if form.bio.data
            else None
        )

        user.role = (
            form.role.data
        )


        # -----------------------------------------
        # PROFILE IMAGE
        # -----------------------------------------

        image = form.profile_image.data

        if image and image.filename:

            filename = secure_filename(
                image.filename
            )

            extension = os.path.splitext(
                filename
            )[1].lower()

            unique_filename = (
                f"{uuid.uuid4().hex}"
                f"{extension}"
            )

            upload_folder = current_app.config[
                "PROFILE_IMAGE_FOLDER"
            ]

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                upload_folder,
                unique_filename
            )

            image.save(
                save_path
            )


            # -------------------------------------
            # DELETE OLD IMAGE
            # -------------------------------------

            if (
                user.profile_image
                and user.profile_image != "default.png"
            ):

                old_image_path = os.path.join(
                    current_app.config[
                        "PROFILE_IMAGE_FOLDER"
                    ],
                    user.profile_image
                )

                if os.path.exists(
                    old_image_path
                ):

                    os.remove(
                        old_image_path
                    )


            # -------------------------------------
            # SAVE NEW IMAGE
            # -------------------------------------

            user.profile_image = (
                unique_filename
            )


        # -----------------------------------------
        # SAVE CHANGES
        # -----------------------------------------

        try:

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            current_app.logger.exception(
                "Error updating user: %s",
                error
            )

            flash(
                "Unable to update the user. "
                "Please try again.",
                "danger"
            )

            return render_template(
                "admin/edit_user.html",
                form=form,
                user=user
            )


        flash(
            "User updated successfully.",
            "success"
        )


        return redirect(
            url_for(
                "admin.view_user",
                user_id=user.id
            )
        )


    # ---------------------------------------------
    # DISPLAY EDIT PAGE
    # ---------------------------------------------

    return render_template(
        "admin/edit_user.html",
        form=form,
        user=user
    )


# =====================================================
# ACTIVATE / DEACTIVATE USER
# =====================================================

@admin_bp.route(
    "/users/toggle-status/<int:user_id>",
    methods=["POST"]
)
@login_required
@admin_required
def toggle_user_status(user_id):

    user = User.query.get_or_404(
        user_id
    )


    # ---------------------------------------------
    # PREVENT SELF-DEACTIVATION
    # ---------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot deactivate your own account.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )


    # ---------------------------------------------
    # TOGGLE STATUS
    # ---------------------------------------------

    if user.status == "active":

        user.status = "inactive"

        message = (
            f"{user.full_name}'s account "
            f"has been deactivated."
        )

    else:

        user.status = "active"

        message = (
            f"{user.full_name}'s account "
            f"has been activated."
        )


    # ---------------------------------------------
    # SAVE
    # ---------------------------------------------

    db.session.commit()


    flash(
        message,
        "success"
    )


    return redirect(
        url_for("admin.users")
    )


# =====================================================
# DELETE USER
# =====================================================

@admin_bp.route(
    "/users/delete/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(
        user_id
    )


    # ---------------------------------------------
    # PREVENT SELF-DELETION
    # ---------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )


    # ---------------------------------------------
    # DELETE
    # ---------------------------------------------

    if request.method == "POST":

        # -----------------------------------------
        # DELETE PROFILE IMAGE
        # -----------------------------------------

        if (
            user.profile_image
            and user.profile_image != "default.png"
        ):

            image_path = os.path.join(
                current_app.config[
                    "PROFILE_IMAGE_FOLDER"
                ],
                user.profile_image
            )

            if os.path.exists(
                image_path
            ):

                os.remove(
                    image_path
                )


        # -----------------------------------------
        # DELETE DATABASE RECORD
        # -----------------------------------------

        db.session.delete(
            user
        )

        db.session.commit()


        flash(
            f"{user.full_name}'s account has been deleted.",
            "success"
        )


        return redirect(
            url_for("admin.users")
        )


    # ---------------------------------------------
    # CONFIRMATION PAGE
    # ---------------------------------------------

    return render_template(
        "admin/delete_user.html",
        user=user
    )