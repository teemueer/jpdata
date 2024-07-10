import sqlalchemy.dialects.postgresql as postgres
import click
from datetime import datetime, timezone
from app import db
from app.cli import bp
from app.dics.model import Dic


@bp.cli.group()
def dics():
    pass


@dics.command()
@click.argument("name")
@click.argument("filepath")
def add(name, filepath):
    """Insert dictionary pages"""

    print(f"*** Parsing {filepath}")
    dictionaries = []
    page = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                indexes = line.split("-")
                idx_start = indexes[0]
                idx_end = indexes[1] if len(indexes) == 2 else indexes[0]

                dictionaries.append(
                    {
                        "name": name,
                        "page": page,
                        "idx_start": idx_start,
                        "idx_end": idx_end,
                    }
                )

            page += 1

    print("*** Inserting dictionary pages")
    stmt = postgres.insert(Dic).values(dictionaries)

    update_dict = {
        "name": getattr(stmt.excluded, "name"),
        "page": getattr(stmt.excluded, "page"),
        "idx_start": getattr(stmt.excluded, "idx_start"),
        "idx_end": getattr(stmt.excluded, "idx_end"),
        "time_updated": datetime.now(timezone.utc),
    }

    stmt = stmt.on_conflict_do_update(constraint="uq_name_page", set_=update_dict)
    db.session.execute(stmt)
    db.session.commit()
