import os
import gzip
import xml.etree.ElementTree as ET
import sqlalchemy.dialects.postgresql as postgres
from urllib.request import urlretrieve
from app import db
from app.cli import bp
from app.characters.models import Character, Meaning, Reading, Variant

@bp.cli.group()
def character():
    pass

@character.command()
def insert():
    """Insert characters from KANJIDIC"""

    characters = []
    readings = []
    meanings = []
    variants = []

    def parse_node(node, _type):
        results = {}
        for e in node:
            results[e.get(_type)] = e.text
        return results

    def parse_misc(node, literal):
        misc = {}
        for e in node:
            if e.tag == "grade":
                misc["grade"] = e.text
            elif e.tag == "stroke_count":
                if "stroke_count" not in misc:
                    misc["stroke_count"] = e.text
            elif e.tag == "rad_name":
                readings.append({
                    "r_type": "radical",
                    "reading": e.text,
                    "character_literal": literal,
                })
            elif e.tag == "variant":
                var_type = e.get("var_type")
                if var_type in ("jis208", "jis212", "jis213", "nelson_c"):
                    variants.append({
                        "var_type": var_type,
                        "variant": e.text,
                        "character_literal": literal,
                    })
        return misc

    def parse_reading_meaning(node, literal):
        for e in node:
            if e.tag == "rmgroup":
                for rm in e:
                    if rm.tag == "reading":
                        r_type = rm.get("r_type")
                        readings.append({
                            "r_type": r_type,
                            "reading": rm.text,
                            "character_literal": literal,
                        })
                    elif rm.tag == "meaning":
                        m_lang = rm.get("m_lang", "en")
                        if m_lang == "en":
                            meanings.append({
                                "meaning": rm.text,
                                "character_literal": literal
                            })
            elif e.tag == "nanori":
                readings.append({
                    "r_type": "nanori",
                    "reading": e.text,
                    "character_literal": literal,
                })

    url = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"

    if not os.path.exists("data"):
        os.makedirs("data")

    filepath = os.path.join("data", "kanjidic2.xml.gz")
    if not os.path.exists(filepath):
        print(f"*** Downloading {url}")
        urlretrieve(url, filepath)

    print(f"*** Parsing KANJIDIC")
    with gzip.open(filepath, "r") as f:
        tree = ET.parse(f)
        for character in tree.iter("character"):
            for e in character:
                if e.tag == "literal":
                    literal = e.text
                elif e.tag == "codepoint":
                    codepoints = parse_node(e, "cp_type")
                elif e.tag == "radical":
                    radicals = parse_node(e, "rad_type")
                elif e.tag == "misc":
                    misc = parse_misc(e, literal)
                elif e.tag == "dic_number":
                    dic_refs = parse_node(e, "dr_type")
                elif e.tag == "reading_meaning":
                    parse_reading_meaning(e, literal)

            characters.append({
                "literal": literal,
                "ucs": codepoints["ucs"],
                "jis208": codepoints.get("jis208"),
                "jis212": codepoints.get("jis212"),
                "jis213": codepoints.get("jis213"),
                "radical": chr(0x2F00 + int(radicals.get("classical")) - 1),
                "stroke_count": misc["stroke_count"],
                "grade": misc.get("grade"),
                "nelson_c": dic_refs.get("nelson_c"),
                "nelson_n": dic_refs.get("nelson_n"),
                "heisig": dic_refs.get("heisig"),
                "heisig6": dic_refs.get("heisig6"),
                "halpern_kkd": dic_refs.get("halpern_kkd"),
                "halpern_kkld_2ed": dic_refs.get("halpern_kkld_2ed"),
            })

    print(f"*** Inserting characters")
    stmt = postgres.insert(Character).values(characters).on_conflict_do_nothing(index_elements=["literal"])
    db.session.execute(stmt)

    print(f"*** Inserting meanings")
    stmt = postgres.insert(Meaning).values(meanings).on_conflict_do_nothing(constraint="uq_meaning_character")
    db.session.execute(stmt)

    print(f"*** Inserting readings")
    stmt = postgres.insert(Reading).values(readings).on_conflict_do_nothing(constraint="uq_type_reading_character")
    db.session.execute(stmt)

    print(f"*** Inserting variants")
    stmt = postgres.insert(Variant).values(variants).on_conflict_do_nothing(constraint="uq_type_variant_character")
    db.session.execute(stmt)

    db.session.commit()
