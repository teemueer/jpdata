import json
import jsonschema
import sqlalchemy.dialects.postgresql as postgres
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.mnemonics import bp
from app.mnemonics.model import Mnemonic
from app.mnemonics.forms import MnemonicFiltersForm
from app.forms import DeleteForm, ImportForm

mnemonics_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "character_literal": {"type": "string"},
            "keyword": {"type": "string"},
            "story": {"type": ["string", "null"]},
        },
        "required": ["character_literal", "keyword"],
    },
}

@bp.route("/mnemonics")
@login_required
def mnemonics():
    filters = MnemonicFiltersForm(request.args)
    if not filters.validate():
        flash("Invalid filters", "error")
        return redirect(url_for("mnemonics.mnemonics"))

    mnemonics = Mnemonic.filter(filters)

    return render_template("mnemonics.html", mnemonics=mnemonics, filters=filters)

@bp.route("/mnemonics/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    mnemonic = db.session.get(Mnemonic, id)
    if not mnemonic:
        abort(404)
    elif mnemonic.user != current_user:
        abort(401)

    form = DeleteForm()
    if form.validate_on_submit():
        if form.yes.data:
            db.session.delete(mnemonic)
            db.session.commit()
            flash("Mnemonic deleted")
            
        literal = request.args.get("literal")
        if literal:
            return redirect(url_for("characters.character", literal=literal))
        return redirect(url_for("mnemonics.mnemonic"))

    return render_template("delete.html", obj=mnemonic, form=form)

@bp.route("/mnemonics/import", methods=["GET", "POST"])
@login_required
def import_mnemonics():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file

        try:
            mnemonics = json.load(file.data)
            jsonschema.validate(mnemonics, mnemonics_schema)
        except:
            flash("Malformed file", "error")
            return redirect(url_for("mnemonics.import_mnemonics"))

        for mnemonic in mnemonics:
            mnemonic["user_id"] = current_user.id
            mnemonic["story"] = mnemonic.get("story")

        stmt = postgres.insert(Mnemonic).values(mnemonics)
        if form.update.data:
            update_dict = {
                "keyword": getattr(stmt.excluded, "keyword"),
                "story": getattr(stmt.excluded, "story"),
                "time_updated": datetime.now(timezone.utc),
            }
            stmt = stmt.on_conflict_do_update(constraint="uq_user_character", set_=update_dict)
        else:
            stmt.on_conflict_do_nothing()

        db.session.execute(stmt)
        db.session.commit()
        flash("Mnemonics imported")
        return redirect(url_for("mnemonics.mnemonics"))

    return render_template("import.html", title="Import mnemonics", form=form)