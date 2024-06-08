from typing_extensions import Annotated
from sqlalchemy import String, select, nulls_last, or_, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from datetime import datetime, timezone
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user

str_1 = Annotated[str, 1]
str_4 = Annotated[str, 4]
str_8 = Annotated[str, 8]
str_16 = Annotated[str, 16]
str_32 = Annotated[str, 32]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]
str_1024 = Annotated[str, 1024]

class Base(DeclarativeBase):
    time_created: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    time_updated: Mapped[datetime | None] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    registry = registry(
        type_annotation_map={
            str_1: String(1),
            str_4: String(4),
            str_8: String(8),
            str_16: String(16),
            str_32: String(32),
            str_64: String(64),
            str_128: String(128),
            str_256: String(256),
            str_512: String(512),
            str_1024: String(1024),
        }
    )

    @classmethod
    def filter(cls, form, user_required=True):
        q = select(cls)

        if user_required:
            q = q.where(cls.user == current_user)

        filters = dict(zip(form._fields, [getattr(form, f).data for f in form._fields]))

        if search := filters.get("search"):
            where = []
            for column in cls.searchable_columns():
                where.append(column.ilike(f"%{search}%"))
            q = q.where(or_(*where))

        order_by = filters.get("order_by", "time_updated")
        desc = filters.get("desc")
        if column := getattr(cls, order_by):
            if column.type.python_type == str:
                column = func.lower(column)
            column = column.desc() if desc else column
            q = q.order_by(nulls_last(column), cls.id.desc())

        page = request.args.get("page", 1, type=int)
        per_page = filters.get("per_page")

        results = db.paginate(
            q,
            page=page,
            per_page=per_page,
            error_out=False,
        )

        return results

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def searchable_columns(self):
        return []

db = SQLAlchemy(model_class=Base)
migrate = Migrate()