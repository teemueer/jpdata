from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Käyttäjätunnus",
        validators=[DataRequired("Pakollinen kenttä")],
    )

    password = PasswordField(
        "Salasana",
        validators=[DataRequired("Pakollinen kenttä")],
    )

    remember_me = BooleanField("Muista kirjautuminen")

    recaptcha = RecaptchaField()

    submit = SubmitField("Kirjaudu")
