from typing import Optional
from tulip.entities.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Chat(Base):
    __tablename__ = "chats"

    id = Mapped[int] = mapped_column(primary_key=True)
    title = Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Chat(id={self.id!r}, username={self.title!r})"
