import json
import jsonschema
import sqlalchemy.dialects.postgresql as postgres
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime, timezone
from app import db
from app.mnemonics import bp
from app.mnemonics.model import Mnemonic
from app.forms import ImportForm

mnemonics_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "literal": {"type": "string"},
            "keyword": {"type": "string"},
            "story": {"type": ["string", "null"]},
        },
        "required": ["literal", "keyword"],
    },
}


@bp.route("/mnemonics/import", methods=["GET", "POST"])
@login_required
def import_mnemonics():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file

        print(file)

        try:
            mnemonics = json.load(file.data)
            jsonschema.validate(mnemonics, mnemonics_schema)
        except:
            flash("Malformed file", "error")
            return redirect(url_for("mnemonics.import_mnemonics"))

        for mnemonic in mnemonics:
            print(mnemonic)
            mnemonic["character_literal"] = mnemonic.get("literal")
            del mnemonic["literal"]
            mnemonic["user_id"] = current_user.id
            mnemonic["story"] = mnemonic.get("story")

        stmt = postgres.insert(Mnemonic).values(mnemonics)
        update_dict = {
            "keyword": getattr(stmt.excluded, "keyword"),
            "story": getattr(stmt.excluded, "story"),
            "time_updated": datetime.now(timezone.utc),
        }
        stmt = stmt.on_conflict_do_update(
            constraint="uq_user_character", set_=update_dict
        )
        db.session.execute(stmt)
        db.session.commit()
        flash("Mnemonics imported")
        return redirect(url_for("main.index"))

    return render_template("import.html", form=form)
