from telegram import Update, User
from telegram.constants import MessageOriginType
from telegram.ext import ContextTypes

from tulip.db import users as user_repo


async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message

    user_repo.update_user(msg.from_user.id, msg.from_user.username, chat.id, chat.title)

    if msg.reply_to_message:
        user_repo.update_user(
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
            chat.id,
            chat.title,
        )

    if msg.forward_origin and msg.forward_origin.type == MessageOriginType.USER:
        forwarded_user: User = msg.forward_origin.sender_user
        user_repo.update_user(forwarded_user.id, forwarded_user.username)
