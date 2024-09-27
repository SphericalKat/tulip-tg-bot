from typing import Optional
from tulip.entities.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id = Mapped[int] = mapped_column(primary_key=True)
    username = Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
