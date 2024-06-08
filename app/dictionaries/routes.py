import os
from flask import abort, render_template, send_from_directory, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.dictionaries import bp
from app.dictionaries.model import Dictionary
from app.words.model import Word
from app.words.forms import NewWordForm

@bp.route("/dictionaries/<string:name>/idx/<int:idx>", methods=["GET", "POST"])
@login_required
def idx(name, idx):
    dictionaries = db.session.query(Dictionary) \
        .where(
            Dictionary.name == name,
            idx >= Dictionary.idx_start,
            idx <= Dictionary.idx_end
        ).order_by(Dictionary.idx_start).all()
    
    if not dictionaries:
        abort(404)

    if dictionaries[-1].idx_end == idx:
        extra = db.session.query(Dictionary) \
            .where(
                Dictionary.name == name,
                Dictionary.page == dictionaries[-1].page + 1
            ).scalar()
        dictionaries.append(extra)

    form = NewWordForm()
    if form.validate_on_submit():
        kanji = form.kanji.data
        kana = form.kana.data
        meaning = form.meaning.data

        word = db.session.query(Word). \
            where(Word.kanji == kanji, Word.kana == kana, Word.user == current_user).scalar()

        if word:
            word.meaning = meaning
            flash("Word meaning updated")
        else:
            word = Word(
                kanji=form.kanji.data,
                kana=form.kana.data,
                meaning=form.meaning.data,
                user=current_user,
            )
            flash("Word saved")

        db.session.add(word)
        db.session.commit()
        return redirect(url_for("dictionaries.idx", name=name, idx=idx))

    return render_template("dictionaries.html", name=name, dictionaries=dictionaries, form=form)

@bp.route("/dictionaries/<string:name>/page/<int:page>")
@login_required
def page(name, page):
    dictionaries = db.session.query(Dictionary) \
        .where(
            Dictionary.name == name,
            Dictionary.page == page
        ).scalar()

    if not dictionaries:
        abort(404)

    filename = os.path.join(name, f"{page:04d}.jpg")
    return send_from_directory("../data", filename)
