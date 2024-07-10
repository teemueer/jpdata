from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from app import db
from app.database import str_1, str_8, str_32, str_64, str_128

if TYPE_CHECKING:
    from app.mnemonics.model import Mnemonic


class Character(db.Model):
    __tablename__ = "characters"

    literal: Mapped[str_1] = mapped_column(primary_key=True)

    ucs: Mapped[str_8] = mapped_column(unique=True)
    jis208: Mapped[str_8 | None] = mapped_column(unique=True)
    jis212: Mapped[str_8 | None] = mapped_column(unique=True)
    jis213: Mapped[str_8 | None] = mapped_column(unique=True)

    radical: Mapped[str_1]
    stroke_count: Mapped[int]
    grade: Mapped[int | None]
    freq: Mapped[int | None]
    jlpt: Mapped[int | None]

    nelson_c: Mapped[int | None] = mapped_column(index=True)
    nelson_n: Mapped[int | None] = mapped_column(index=True)
    heisig: Mapped[int | None] = mapped_column(index=True)
    heisig6: Mapped[int | None] = mapped_column(index=True)
    halpern_kkd: Mapped[int | None] = mapped_column(index=True)
    halpern_kkld_2ed: Mapped[int | None] = mapped_column(index=True)
    kanjikirja: Mapped[int | None] = mapped_column(index=True)

    heisig_keyword: Mapped[str_32 | None] = mapped_column(index=True)
    my_keyword: Mapped[str_128 | None] = mapped_column(index=True)

    parts: Mapped[str_32 | None] = mapped_column(index=True)

    meanings: WriteOnlyMapped["Meaning"] = relationship(back_populates="character")
    readings: WriteOnlyMapped["Reading"] = relationship(back_populates="character")
    variants: WriteOnlyMapped["Variant"] = relationship(back_populates="character")
    decompositions: WriteOnlyMapped["Decomposition"] = relationship(
        back_populates="character"
    )
    mnemonics: WriteOnlyMapped["Mnemonic"] = relationship(back_populates="character")

    @classmethod
    def search_from(cls):
        return [(Reading, "reading")]


class Meaning(db.Model):
    __tablename__ = "meanings"

    id: Mapped[int] = mapped_column(primary_key=True)

    meaning: Mapped[str_128] = mapped_column(index=True)

    character_literal: Mapped[str_1] = mapped_column(ForeignKey("characters.literal"))
    character: Mapped["Character"] = relationship(back_populates="meanings")

    __table_args__ = (
        UniqueConstraint("meaning", "character_literal", name="uq_meaning_character"),
    )

    @classmethod
    def searchable_columns(cls):
        return [cls.meaning]


class Reading(db.Model):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)

    r_type: Mapped[str_8] = mapped_column(index=True)
    reading: Mapped[str_32] = mapped_column(index=True)

    character_literal: Mapped[str_1] = mapped_column(ForeignKey("characters.literal"))
    character: Mapped["Character"] = relationship(back_populates="readings")

    __table_args__ = (
        UniqueConstraint(
            "r_type", "reading", "character_literal", name="uq_type_reading_character"
        ),
    )


class Variant(db.Model):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True)

    var_type: Mapped[str_8] = mapped_column(index=True)
    variant: Mapped[str_8] = mapped_column(index=True)

    character_literal: Mapped[str_1] = mapped_column(ForeignKey("characters.literal"))
    character: Mapped["Character"] = relationship(back_populates="variants")

    __table_args__ = (
        UniqueConstraint(
            "var_type",
            "variant",
            "character_literal",
            name="uq_type_variant_character",
        ),
    )


class Decomposition(db.Model):
    __tablename__ = "decompositions"

    id: Mapped[int] = mapped_column(primary_key=True)

    decomposition: Mapped[str_32] = mapped_column(index=True)

    character_literal: Mapped[str_1] = mapped_column(ForeignKey("characters.literal"))
    character: Mapped["Character"] = relationship(back_populates="decompositions")

    __table_args__ = (
        UniqueConstraint(
            "decomposition",
            "character_literal",
            name="uq_decomposition_character",
        ),
    )
