from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class ExportForm(FlaskForm):
    export = SelectField(
        "Export",
        choices=[
            ("anki", "Anki"),
            ("mnemonics_words", "Mnemonics and words"),
            ("mnemonics", "Mnemonics"),
            ("words", "Words"),
        ],
        default="anki",
    )

    submit = SubmitField("Export")