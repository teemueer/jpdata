import logging
from flask import request, flash, redirect, url_for, render_template, abort, Response
from flask_login import current_user
from sqlalchemy.orm import joinedload
from app import db
from app.characters import bp
from app.characters.models import Character
from app.characters.form import CharactersForm, KeywordForm, StoryForm
from app.mnemonics.model import Mnemonic
from app.words.model import Word


@bp.route("/characters")
def characters():
    form = CharactersForm(request.args)

    logging.warning(
        f"{request.remote_addr}: {form.search.data}/{form.limit_to.data}/{form.per_page.data}"
    )

    if not form.validate():
        flash("Virheelliset suodattimet", "danger")
        return redirect(url_for("characters.characters"))

    characters = Character.find(form)
    return render_template("characters.html", form=form, characters=characters)


def character_authenticated(character):
    mnemonic = (
        db.session.query(Mnemonic)
        .filter(
            Mnemonic.character_literal == character.literal,
            Mnemonic.user == current_user,
        )
        .scalar()
    )

    words = (
        db.session.query(Word)
        .filter(
            Word.kanji.ilike(f"%{character.literal}%"),
            Word.user == current_user,
        )
        .order_by(Word.kana)
        .all()
    )

    keyword_form = KeywordForm()
    if keyword_form.submit.data and keyword_form.validate_on_submit():
        if not keyword_form.keyword.data.strip():
            keyword_form.keyword.data = character.my_keyword

        if mnemonic:
            mnemonic.keyword = keyword_form.keyword.data
        else:
            mnemonic = Mnemonic(
                character_literal=character.literal,
                keyword=keyword_form.keyword.data,
                user=current_user,
            )

        db.session.add(mnemonic)
        db.session.commit()
        return redirect(url_for("characters.character", literal=character.literal))

    story_form = StoryForm()
    if story_form.submit.data and story_form.validate_on_submit():
        if not story_form.story.data.strip():
            story_form.story.data = None

        if mnemonic:
            mnemonic.story = story_form.story.data
        else:
            mnemonic = Mnemonic(
                character_literal=character.literal,
                keyword=character.my_keyword,
                story=story_form.story.data,
                user=current_user,
            )

        db.session.add(mnemonic)
        db.session.commit()
        return redirect(url_for("characters.character", literal=character.literal))

    if mnemonic:
        keyword_form.keyword.data = mnemonic.keyword
        story_form.story.data = mnemonic.story
    else:
        keyword_form.keyword.data = character.my_keyword

    return mnemonic, words, keyword_form, story_form

def character_anonymous(character):
    return render_template("anonymous/character.html")


@bp.route("/character/<string:literal>", methods=["GET", "POST"])
def character(literal):
    character = db.session.get(Character, literal)
    if not character:
        abort(404)

    if current_user.is_authenticated:
        result = character_authenticated(character)
        if type(result) == Response:
            return result
        mnemonic, words, keyword_form, story_form = result

    readings = db.session.scalars(character.readings.select()).all()
    meanings = db.session.scalars(character.meanings.select()).all()
    decompositions = db.session.scalars(character.decompositions.select()).all()

    variants = []
    for variant in db.session.scalars(character.variants.select()):
        column = getattr(Character, variant.var_type)
        variant_character = (
            db.session.query(Character).filter(column == variant.variant).scalar()
        )
        if variant_character not in variants:
            variants.append(variant_character)

    neighbors = []
    neighbor_type = request.cookies.get("neighbors", "heisig6")
    column = getattr(Character, neighbor_type)
    if idx := getattr(character, neighbor_type):
        neighbors = (
            db.session.query(Character)
            .filter(column.between(idx - 10, idx + 10))
            .order_by(column)
            .all()
        )

    context = {
        "character": character,
        "readings": readings,
        "meanings": meanings,
        "decompositions": decompositions,
        "variants": variants,
        "neighbors": neighbors,
    }

    if current_user.is_authenticated:
        context["keyword_form"] = keyword_form
        context["story_form"] = story_form
        context["mnemonic"] = mnemonic
        context["words"] = words
        return render_template("authenticated/character.html", **context)
    else:
        return render_template("anonymous/character.html", **context)

    """
    if current_user.is_authenticated:
        return render_template(
            "authenticated/character.html",
            character=character,
            mnemonic=mnemonic,
            keyword_form=keyword_form,
            story_form=story_form,
            meanings=meanings,
            readings=readings,
            decompositions=decompositions,
            variants=variants,
            words=words,
            neighbors=neighbors,
        )
    """