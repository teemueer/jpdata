from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.forms import FiltersForm

class NewWordForm(FlaskForm):
    kanji = StringField("Kanji", validators=[DataRequired()])
    kana = StringField("Kana", validators=[DataRequired()])
    meaning = TextAreaField("Meaning")
    submit = SubmitField("Save word")

class UpdateWordForm(FlaskForm):
    kanji = StringField("Kanji", validators=[DataRequired()])
    kana = StringField("Kana", validators=[DataRequired()])
    meaning = TextAreaField("Meaning")
    submit = SubmitField("Update")
    remove = SubmitField("Delete")

class WordFiltersForm(FiltersForm):
    order_by = SelectField(
        "Order by",
        choices=[
            ("kanji", "Kanji"),
            ("kana", "Kana"),
            ("time_updated", "Time updated"),
            ("time_created", "Time created"),
        ],
        default="time_updated",
    )