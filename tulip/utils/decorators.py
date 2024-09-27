from functools import wraps
from telegram import Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.ext import ContextTypes


def bot_can_restrict(func):
    @wraps(func)
    async def promote_rights(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        bot_chat_member = await update.effective_chat.get_member(context.bot.id)
        if (
            bot_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and bot_chat_member.can_restrict_members
        ):
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "I can't restrict members in this chat. Make sure I'm an admin and have the necessary permissions."
            )

    return promote_rights


def user_can_restrict(func):
    @wraps(func)
    async def promote_rights(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user_chat_member = await update.effective_chat.get_member(
            update.effective_user.id
        )
        if (
            user_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and user_chat_member.can_restrict_members
        ) or user_chat_member.status == ChatMemberStatus.OWNER:
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "You don't have the necessary permissions to restrict members in this chat."
            )

    return promote_rights


def require_group_chat(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        if update.effective_chat.type == ChatType.PRIVATE:
            await update.effective_message.reply_text(
                "This command can only be used in groups."
            )
        else:
            return await func(update, context)

    return wrapped
