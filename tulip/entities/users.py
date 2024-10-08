from typing import Optional

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tulip.entities.base import Base

chat_members = Table(
    "chat_members",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "chat_id",
        ForeignKey("chats.id"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]]

    chats: Mapped[list["Chat"]] = relationship(
        secondary=chat_members,
        back_populates="users",
        cascade="all",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]

    users: Mapped[list["User"]] = relationship(
        secondary=chat_members,
        back_populates="chats",
        cascade="all",
    )

    def __repr__(self) -> str:
        return f"Chat(id={self.id!r}, username={self.title!r})"
