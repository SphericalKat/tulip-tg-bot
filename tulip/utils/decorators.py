from functools import wraps

from telegram import Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.ext import ContextTypes


def bot_can_restrict(func):
    @wraps(func)
    async def wrapped(
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

    return wrapped


def bot_can_promote(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        bot_chat_member = await update.effective_chat.get_member(context.bot.id)
        if (
            bot_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and bot_chat_member.can_promote_members
        ):
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "I can't promote members in this chat. Make sure I'm an admin and have the necessary permissions."
            )

    return wrapped


def bot_can_pin(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        bot_chat_member = await update.effective_chat.get_member(context.bot.id)
        if (
            bot_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and bot_chat_member.can_pin_messages
        ):
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "I can't pin messages in this chat. Make sure I'm an admin and have the necessary permissions."
            )

    return wrapped


def user_can_pin(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user_chat_member = await update.effective_chat.get_member(
            update.effective_user.id
        )
        if (
            user_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and user_chat_member.can_pin_messages
        ) or user_chat_member.status == ChatMemberStatus.OWNER:
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "You don't have the necessary permissions to pin messages in this chat."
            )

    return wrapped


def user_can_promote(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user_chat_member = await update.effective_chat.get_member(
            update.effective_user.id
        )
        if (
            user_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and user_chat_member.can_promote_members
        ) or user_chat_member.status == ChatMemberStatus.OWNER:
            return await func(update, context)
        else:
            await update.effective_message.reply_text(
                "You don't have the necessary permissions to promote members in this chat."
            )

    return wrapped


def user_can_restrict(func):
    @wraps(func)
    async def wrapped(
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

    return wrapped


def require_group_chat(func):
    @wraps(func)
    async def wrapped(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        if update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.effective_message.reply_text(
                "This command can only be used in groups."
            )
        else:
            return await func(update, context)

    return wrapped
