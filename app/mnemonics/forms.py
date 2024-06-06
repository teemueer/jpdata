from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.forms import FiltersForm

class MnemonicForm(FlaskForm):
    keyword = StringField("Keyword", validators=[DataRequired()])
    story = TextAreaField("Story")
    submit = SubmitField("Save mnemonic")
    remove = SubmitField("Delete")

class MnemonicFiltersForm(FiltersForm):
    order_by = SelectField(
        "Order by",
        choices=[
            ("keyword", "Keyword"),
            ("time_updated", "Time updated"),
            ("time_created", "Time created"),
        ],
        default="time_updated",
    )