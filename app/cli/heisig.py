import os
from urllib.request import urlretrieve
from app import db
from app.cli import bp
from app.characters.models import Character

@bp.cli.group()
def heisig():
    pass

@heisig.command()
def insert():
    """Insert official keywords from Remembering the Kanji"""

    url = "https://raw.githubusercontent.com/sdcr/heisig-kanjis/master/heisig-kanjis.csv"

    if not os.path.exists("data"):
        os.makedirs("data")

    filepath = os.path.join("data", "heisig.csv")
    if not os.path.exists(filepath):
        print(f"*** Downloading {url}")
        urlretrieve(url, filepath)

    print("*** Parsing and inserting keywords")
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            fields = line.split(",")

            literal = fields[0]
            character = db.session.query(Character).where(Character.literal == literal).scalar()
            if not character:
                continue

            keyword_5th_ed = fields[3]
            keyword_6th_ed = fields[4]
            heisig_keyword = keyword_6th_ed if keyword_6th_ed else keyword_5th_ed

            character.heisig_keyword = heisig_keyword
            db.session.add(character)

    db.session.commit()
