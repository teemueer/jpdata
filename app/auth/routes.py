import logging
from flask import current_app, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from urllib.parse import urlsplit
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.users.model import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_app.debug:
        del form.recaptcha

    if form.validate_on_submit():
        user = (
            db.session.query(User).where(User.username == form.username.data).scalar()
        )

        if user is None or not user.check_password(form.password.data):
            logging.warning(
                f"{request.remote_addr} tried {form.username.data}/{form.username.data}"
            )
            flash("Virheellinen käyttäjätunnus tai salasana", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
