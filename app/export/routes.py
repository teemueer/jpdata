import sqlalchemy as sa
from io import BytesIO
from flask import flash, render_template, redirect, url_for, send_file
from flask_login import current_user
from app import db
from app.export import bp
from app.export.forms import ExportForm
from app.mnemonics.model import Mnemonic
from app.characters.models import Character

def export_anki():
    import time
    start_time = time.time()

    all_words = db.session.scalars(current_user.words.select()).all()

    q = sa.select(Mnemonic, Character) \
        .join(
            Character,
            Mnemonic.character_literal == Character.literal,
        ).where(Mnemonic.user == current_user) \
        .order_by(Character.heisig6)
    
    cards = []
    for mnemonic, character in db.session.execute(q):
        card = [
            character.literal,
            mnemonic.keyword,
            mnemonic.story or "",
        ]

        words = [word for word in all_words if character.literal in word.kanji]
        words_str = ""
        for word in words:
            meaning = word.meaning.replace("\n", "<br>").replace("\r", "") or ""
            words_str += f'<details class="word"><summary><span class="kanji">{word.kanji}</span><span class="kana">【{word.kana}】</span></summary><div class="meaning">{word.meaning or ""}</div></details>'
        card.append(words_str)

        cards.append(card)

    cards_str = "\n".join(["\t".join(card) for card in cards])
    file = BytesIO(cards_str.encode())

    print("export_anki took", time.time() - start_time)
    return file

@bp.route("/export", methods=["GET", "POST"])
def export():
    form = ExportForm()
    if form.validate_on_submit():
        export_type = form.export.data
        if export_type == "anki":
            file = export_anki()
        flash("Export successful")
        return send_file(file, download_name="jpdata.tsv", as_attachment=True)
        #return redirect(url_for("export.export"))

    return render_template("export.html", form=form)