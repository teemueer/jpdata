from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import RadioField, BooleanField, IntegerField, SelectField
from wtforms.validators import Optional, NumberRange


class CustomizeForm(FlaskForm):
    theme = RadioField(
        "Sivuston teema",
        choices=[("light", "Vaalea"), ("dark", "Tumma")],
        default="light",
    )

    nanori = BooleanField("Nanori", default=False)
    pinyin = BooleanField("Pinyin", default=False)

    krad = BooleanField("KRAD", default=True)
    cjk = BooleanField("CJK", default=True)
    variants = BooleanField("Variantit", default=True)

    heisig = BooleanField("Remembering the Kanji indeksi", default=True)
    kanjikirja = BooleanField("Suuri kanjikirja: Uudistettu laitos", default=True)
    halpern_kkd = BooleanField("Kodansha Kanji Dictionary indeksi", default=True)
    nelson_n = BooleanField("New Nelson indeksi", default=True)
    jis = BooleanField("JIS-koodaus", default=True)

    neighbors = SelectField(
        "Naapurilista",
        choices=[
            ("heisig6", "Remembering the Kanji, 6. painos"),
            ("kanjikirja", "Suuri kanjikirja: Uudistettu laitos"),
            ("halpern_kkd", "Kodansha Kanji Dictionary"),
            ("nelson_n", "New Nelson"),
        ],
        default="heisig",
    )

    halpern_kkd_offset = IntegerField(
        "Offset", validators=[NumberRange(0, 9999)], default=59
    )

    nelson_n_offset = IntegerField(
        "Offset", validators=[NumberRange(0, 9999)], default=13
    )

    kanjikirja_offset = IntegerField(
        "Offset", validators=[NumberRange(0, 9999)], default=1
    )
