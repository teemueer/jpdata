from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Optional, Length, ValidationError, DataRequired


class CharactersForm(FlaskForm):
    class Meta:
        csrf = False

    search = StringField("Haku", validators=[Optional()])

    limit_to = SelectField(
        "Rajaus",
        choices=[
            ("heisig6", "Remembering the Kanji, 6. painos"),
            ("heisig", "Remembering the Kanji, 5. painos"),
            ("halpern_kkd", "Kodansha Kanji Dictionary"),
            ("halpern_kkld_2ed", "Kodansha Kanji Learner's Dictionary"),
            ("nelson_n", "New Nelson"),
            ("jis208", "JIS X 208"),
            ("jis212", "JIS X 212"),
            ("jis213", "JIS X 213"),
        ],
        default="heisig6",
    )

    per_page = SelectField(
        "Per sivu",
        choices=[
            (100, "100"),
            (250, "250"),
            (500, "500"),
            (1000, "1000"),
        ],
        default=1000,
        coerce=int,
    )


class KeywordForm(FlaskForm):
    keyword = StringField("Avainsana", validators=[Optional()])
    submit = SubmitField("Tallenna", name="keyword-submit")


class StoryForm(FlaskForm):
    story = TextAreaField("Muistisääntö", validators=[Optional()])
    submit = SubmitField("Tallenna", name="story-submit")
