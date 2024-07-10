from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import RadioField, SelectField, SearchField, SubmitField


class ImportForm(FlaskForm):
    file = FileField(
        "File",
        validators=[
            FileRequired(),
            FileAllowed(["json"], "JSON files only!"),
        ],
        render_kw={"accept": ".json"},
    )

    update = RadioField(
        "Update existing", choices=[(1, "Yes"), (0, "No")], default=1, coerce=int
    )

    submit = SubmitField("Import")
