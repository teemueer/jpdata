from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.database import db
from app.users.model import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.query(User).where(User.username == username.data).scalar()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = db.session.query(User).where(User.email == email.data).scalar()
        if user is not None:
            raise ValidationError("Please use a different email address.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    recaptcha = RecaptchaField()
    submit = SubmitField("Sign In")
