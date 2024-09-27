from telegram import Chat, ChatMember
from telegram.constants import ChatMemberStatus, ChatType


async def is_user_ban_protected(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if chat.type == ChatType.PRIVATE:
        return True

    if not member:
        member = await chat.get_member(user_id)
    return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
