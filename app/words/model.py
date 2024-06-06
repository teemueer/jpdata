from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.database import str_32, str_512

if TYPE_CHECKING:
    from app.users.model import User

class Word(db.Model):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)

    kanji: Mapped[str_32]
    kana: Mapped[str_32]
    meaning: Mapped[str_512 | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="words")

    __table_args__ = (
        UniqueConstraint("kanji", "kana", "user_id", name="uq_kanji_kana_user"),
    )

    @classmethod
    def searchable_columns(cls):
        return [cls.kanji, cls.kana, cls.meaning] 