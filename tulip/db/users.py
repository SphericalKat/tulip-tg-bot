from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tulip import LOGGER
from tulip.db import engine
from tulip.entities.users import Chat, User


def get_userid_by_name(username: str) -> Optional[List[User]]:
    try:
        with Session(engine) as session:
            return (
                session.query(User)
                .filter(func.lower(User.username) == username.lower())
                .all()
            )
    except Exception as e:
        LOGGER.exception("Error getting user by name", e)
        return None


def update_user(
    user_id: int,
    username: str,
    chat_id: Optional[int] = None,
    chat_name: Optional[str] = None,
) -> None:
    with Session(engine) as session:
        # upsert user
        user: User | None = session.query(User).get(user_id)
        if not user:
            user = User(id=user_id, username=username)
            session.add(user)
            session.flush()
        else:
            user.username = username

        # if no chat_id or chat_name, nothing more to do
        if not chat_id or not chat_name:
            session.commit()
            return

        # upsert chat
        chat: Chat | None = session.query(Chat).get(chat_id)
        if not chat:
            chat = Chat(id=chat_id, title=chat_name)
            session.add(chat)
            session.flush()
        else:
            chat.title = chat_name

        # upsert chat member
        query = (
            select(User).join(User.chats).where(User.id == user_id, Chat.id == chat_id)
        )

        member = session.scalars(query).first()
        if not member:
            user.chats.append(chat)

        session.commit()
