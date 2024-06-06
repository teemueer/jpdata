import json
import jsonschema
import sqlalchemy.dialects.postgresql as postgres
from flask import flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.words import bp
from app.words.model import Word
from app.words.forms import NewWordForm, UpdateWordForm, WordFiltersForm
from app.forms import DeleteForm, ImportForm

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

@bp.route("/words", methods=["GET", "POST"])
@login_required
def words():
    filters = WordFiltersForm(request.args)
    if not filters.validate():
        flash("Invalid filters", "error")
        return redirect(url_for("words.words"))

    word_form = NewWordForm()
    if word_form.validate_on_submit():
        word = Word(
            kanji=word_form.kanji.data,
            kana=word_form.kana.data,
            meaning=word_form.meaning.data,
            user=current_user,
        )

        db.session.add(word)
        db.session.commit()
        flash("Word saved")
        return redirect(url_for("words.words"))

    words = Word.filter(filters)

    return render_template(
        "words.html",
        words=words,
        word_form=word_form,
        filters=filters,
    )

@bp.route("/words/<int:id>", methods=["GET", "POST"])
@login_required
def word(id):
    word = db.session.get(Word, id)
    if not word:
        abort(404)
    elif word.user != current_user:
        abort(401)

    literal = request.args.get("literal")
    
    form = UpdateWordForm(obj=word)
    if form.remove.data:
        return redirect(url_for("words.delete", id=word.id, literal=literal))
    elif form.validate_on_submit():
        word.kanji = form.kanji.data
        word.kana = form.kana.data
        word.meaning = form.meaning.data

        db.session.add(word)
        db.session.commit()
        flash("Word updated")

        literal = request.args.get("literal")
        if literal:
            return redirect(url_for("characters.character", literal=literal))
        return redirect(url_for("words.words"))

    return render_template("word.html", word=word, form=form)

@bp.route("/words/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    word = db.session.get(Word, id)
    if not word:
        abort(404)
    elif word.user != current_user:
        abort(401)

    form = DeleteForm()
    if form.validate_on_submit():
        if form.yes.data:
            db.session.delete(word)
            db.session.commit()
            flash("Word deleted")
        
        literal = request.args.get("literal")
        if literal:
            return redirect(url_for("characters.character", literal=literal))
        return redirect(url_for("words.words"))

    return render_template("delete.html", obj=word, form=form)

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
            word["meaning"] = word.get("story")

        stmt = postgres.insert(Word).values(words)
        if form.update.data:
            update_dict = {
                "kanji": getattr(stmt.excluded, "kanji"),
                "kana": getattr(stmt.excluded, "kana"),
                "meaning": getattr(stmt.excluded, "meaning"),
                "time_updated": datetime.now(timezone.utc),
            }
            stmt = stmt.on_conflict_do_update(constraint="uq_kanji_kana_user", set_=update_dict)
        else:
            stmt.on_conflict_do_nothing()

        db.session.execute(stmt)
        db.session.commit()
        flash("Words imported")
        return redirect(url_for("words.words"))

    return render_template("import.html", title="Import words", form=form)