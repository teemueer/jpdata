from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.database import str_1, str_64, str_512

if TYPE_CHECKING:
    from app.characters.models import Character
    from app.users.model import User

class Mnemonic(db.Model):
    __tablename__ = "mnemonics"

    id: Mapped[int] = mapped_column(primary_key=True)

    keyword: Mapped[str_64]
    story: Mapped[str_512 | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="mnemonics")

    character_literal: Mapped[str_1] = mapped_column(ForeignKey("characters.literal"))
    character: Mapped["Character"] = relationship(back_populates="mnemonics")

    __table_args__ = (
        UniqueConstraint("user_id", "character_literal", name="uq_user_character"),
    )

    @classmethod
    def searchable_columns(cls):
        return [cls.keyword, cls.story, cls.character_literal] 
