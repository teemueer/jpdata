import os
import sqlalchemy.dialects.postgresql as postgres
from urllib.request import urlretrieve
from app import db
from app.cli import bp
from app.characters.models import Character, Decomp

@bp.cli.group()
def decomp():
    pass

@decomp.command()
def insert():
    """Insert character decomposition data"""

    longest_decomp = 0

    url = "https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt"

    if not os.path.exists("data"):
        os.makedirs("data")

    filepath = os.path.join("data", "decomp.txt")
    if not os.path.exists(filepath):
        print(f"*** Downloading {url}")
        urlretrieve(url, filepath)

    literals = [character.literal for character in db.session.query(Character).all()]

    print("*** Parsing decomp data")
    decomps = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            fields = line.split("\t")
            literal = fields[1]
            if literal not in literals:
                continue

            for decomp in fields[2:]:
                decomps.append({"decomp": decomp, "character_literal": literal})

    print("*** Inserting decomps")
    stmt = postgres.insert(Decomp).values(decomps).on_conflict_do_nothing(constraint="uq_decomp_character")

    db.session.execute(stmt)
    db.session.commit()
