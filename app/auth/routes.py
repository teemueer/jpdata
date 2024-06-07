from flask import current_app, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit
from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm
from app.users.model import User

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if current_app.debug:
        del form.recaptcha

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if current_app.debug:
        del form.recaptcha

    if form.validate_on_submit():
        user = db.session.query(User).where(User.username == form.username.data).scalar()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash("You have logged in")

        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("auth.login"))
