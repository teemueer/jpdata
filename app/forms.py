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
    update = RadioField("Update existing", choices=[(1, "Yes"), (0, "No")], default=1, coerce=int)
    submit = SubmitField("Import")

class FiltersForm(FlaskForm):
    class Meta:
        csrf = False

    search = SearchField()

    desc = SelectField(
        choices=[(0, "Ascending"), (1, "Descending")],
        default=1,
        coerce=int,
    )

    per_page = SelectField(
        "Per page",
        choices=[
            (10, "10"),
            (20, "20"),
            (50, "50"),
            (100, "100"),
        ],
        default=10,
        coerce=int,
    )

class DeleteForm(FlaskForm):
    yes = SubmitField("Yes")
    no = SubmitField("No")