from flask import Blueprint, request, render_template, redirect, session, url_for
from app.database import db
from app.database.model import User
from app.auth.utils import hash_password, verify_password
from app.utils.helpers import encrypt_imap_password



auth = Blueprint("auth", __name__)


@auth.route("/")
def index():
    return render_template("home.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password = request.form.get("password")
        imap_server = request.form.get("imap_server")
        imap_port = int(request.form.get("imap_port", 993))

        if not all([user_name, email, password, imap_server]):
            return render_template("register.html", error="All fields are required")

        password_hash = hash_password(password)
        imap_password_enc = encrypt_imap_password(password)

        user = User(
            user_name=user_name,
            email=email,
            password_hash=password_hash,
            imap_email=email,
            imap_server=imap_server,
            imap_port=imap_port,
            imap_password_enc=imap_password_enc
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="User not found")

        if verify_password(password, user.password_hash):

            session["user_id"] = user.user_id
            session["user_name"] = user.user_name

            return redirect(url_for("dashboard.user_home"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
