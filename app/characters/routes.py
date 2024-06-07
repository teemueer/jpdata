import sqlalchemy as sa
from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.characters import bp
from app.characters.models import Character
from app.mnemonics.model import Mnemonic
from app.mnemonics.forms import MnemonicForm
from app.words.model import Word
from app.words.forms import NewWordForm

@bp.route("/characters")
@login_required
def characters():
    q = sa.select(Character, Mnemonic) \
        .join(
            Mnemonic,
            sa.and_(
                Character.literal == Mnemonic.character_literal,
                Mnemonic.user == current_user
            ), isouter=True
        ).where(Character.heisig6 != None) \
        .order_by(Character.heisig6)
    characters = db.session.execute(q).all()
    return render_template("characters.html", characters=characters)

@bp.route("/characters/<string:literal>", methods=["GET", "POST"])
@login_required
def character(literal):
    character = db.session.query(Character).where(Character.literal == literal).scalar()
    if not character:
        abort(404)

    decomps = db.session.scalars(character.decomps.select()).all()
    meanings = db.session.scalars(character.meanings.select()).all()
    readings = db.session.scalars(character.readings.select()).all()

    variants = []
    for variant in db.session.scalars(character.variants.select()):
        column = getattr(Character, variant.var_type)
        variant_character = db.session.query(Character).where(column == variant.variant).scalar()
        if variant_character not in variants:
            variants.append(variant_character)

    word_form = NewWordForm()
    if word_form.validate_on_submit():
        if character.literal not in word_form.kanji.data:
            flash("Kanji field must contain the current character", "error")
            return redirect(url_for("characters.character", literal=literal))

        word = Word(
            kanji=word_form.kanji.data,
            kana=word_form.kana.data,
            meaning=word_form.meaning.data,
            user=current_user,
        )

        db.session.add(word)
        db.session.commit()
        flash("Word saved")
        return redirect(url_for("characters.character", literal=literal))

    q = current_user.mnemonics.select().where(Mnemonic.character == character)
    mnemonic = db.session.scalar(q)

    mnemonic_form = MnemonicForm(obj=mnemonic)

    if not mnemonic:
        del mnemonic_form.remove

    if mnemonic_form.validate_on_submit():
        if mnemonic_form.remove.data:
            return redirect(url_for("mnemonics.delete", id=mnemonic.id, literal=literal))
        
        if mnemonic:
            mnemonic.keyword = mnemonic_form.keyword.data
            mnemonic.story = mnemonic_form.story.data
        else:
            mnemonic = Mnemonic(
                keyword=mnemonic_form.keyword.data,
                story=mnemonic_form.story.data,
                user=current_user,
                character=character,
            )

        db.session.add(mnemonic)
        db.session.commit()
        flash("Mnemonic saved")
        return redirect(url_for("characters.character", literal=literal))
    
    words = db.session.scalars(
        current_user.words.select() \
            .where(
                Word.kanji.like(f"%{literal}%")
            ).order_by(Word.kana)
        ).all()
    
    idx = character.heisig6
    if idx:
        neighbor_characters = db.session.query(Character) \
            .where(Character.heisig6.between(abs(idx-10), idx+10)).all()
    else:
        neighbor_characters = []

    return render_template(
        "character.html",
        character=character,
        meanings=meanings,
        decomps=decomps,
        readings=readings,
        variants=variants,
        word_form=word_form,
        mnemonic_form=mnemonic_form,
        words=words,
        neighbor_characters=neighbor_characters,
    )