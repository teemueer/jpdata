from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from app.database import str_16

class Dictionary(db.Model):
    __tablename__ = "dictionaries"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str_16] = mapped_column(index=True)
    page: Mapped[int] = mapped_column(index=True)
    idx_start: Mapped[int] = mapped_column(index=True)
    idx_end: Mapped[int] = mapped_column(index=True)

    __table_args__ = (
        UniqueConstraint("name", "page", name="uq_name_page"),
    )
