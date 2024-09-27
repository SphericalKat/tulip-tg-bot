
from sqlalchemy import ForeignKey
from tulip.entities.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tulip.entities.chat import Chat
from tulip.entities.user import User


class ChatMember(Base):
    __tablename__ = "chat_members"

    user_id = Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id = Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="chats")
    user: Mapped["Chat"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"ChatMember(user_id={self.user_id!r}, chat_id={self.chat_id!r})"
