from typing import TYPE_CHECKING
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from app.database import str_64, str_128, str_256

if TYPE_CHECKING:
    from app.mnemonics.model import Mnemonic
    from app.words.model import Word

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str_64] = mapped_column(index=True, unique=True)
    email: Mapped[str_128] = mapped_column(index=True, unique=True)
    password_hash: Mapped[str_256] = mapped_column(index=True, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    mnemonics: WriteOnlyMapped["Mnemonic"] = relationship(back_populates="user")
    words: WriteOnlyMapped["Word"] = relationship(back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
