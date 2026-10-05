from functools import wraps

from flask import (
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user
)


def admin_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not current_user.is_authenticated:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        if current_user.role != "Administrator":

            flash(
                "Access denied. Administrator privileges required.",
                "danger"
            )

            return redirect(
                url_for("main.home")
            )

        return view(*args, **kwargs)

    return wrapped_view