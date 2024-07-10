import json
import jsonschema
import sqlalchemy.dialects.postgresql as postgres
from flask import flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.words import bp
from app.words.model import Word
from app.forms import ImportForm

words_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "kanji": {"type": "string"},
            "kana": {"type": "string"},
            "meaning": {"type": ["string", "null"]},
        },
        "required": ["kanji", "kana"],
    },
}


@bp.route("/words/import", methods=["GET", "POST"])
@login_required
def import_words():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file

        try:
            words = json.load(file.data)
            jsonschema.validate(words, words_schema)
        except:
            flash("Malformed file", "error")
            return redirect(url_for("words.import_mnemonics"))

        for word in words:
            word["user_id"] = current_user.id

        stmt = postgres.insert(Word).values(words)
        if form.update.data:
            update_dict = {
                "kanji": getattr(stmt.excluded, "kanji"),
                "kana": getattr(stmt.excluded, "kana"),
                "meaning": getattr(stmt.excluded, "meaning"),
                "time_updated": datetime.now(timezone.utc),
            }
            stmt = stmt.on_conflict_do_update(
                constraint="uq_kanji_kana_user", set_=update_dict
            )
        else:
            stmt = stmt.on_conflict_do_nothing()

        print(words)

        db.session.execute(stmt)
        db.session.commit()
        flash("Words imported")
        return redirect(url_for("main.index"))

    return render_template("import.html", title="Import words", form=form)
