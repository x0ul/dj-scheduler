import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response)
from werkzeug.security import check_password_hash, generate_password_hash

from dj_scheduler.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"yup": "huh"}))


@bp.route("/register", methods=["POST"])
def register():
    req = request.get_json()
    username = req["username"]
    password = req["password"]
    db = get_db()
    error = None

    if not username:
        error = "username is required"
    elif not password:
        error = "password is required"

    if not error:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
        except db.IntegrityError:
            error = f"user {username} is already registered"

    return make_response(jsonify({"error": error}))


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if not user:
            error = "incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "incorrect password"

        if not error:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
