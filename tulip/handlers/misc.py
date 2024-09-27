from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import MessageOriginType

from tulip.utils.extraction import extract_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm Tulip - A bot to help manage your groups! Use the /help command to see what I can do!",
    )


async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = await extract_user(update.effective_message, context.args)
    if user_id:
        if (
            update.effective_message.reply_to_message
            and update.effective_message.reply_to_message.forward_origin
            and update.effective_message.reply_to_message.forward_origin.type
            == MessageOriginType.USER
        ):
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_origin.sender_user
            await update.effective_message.reply_text(
                f"{user1.first_name}'s id is <code>{user1.id}</code>.\nThe forwarded user, {user2.first_name} has an ID of <code>{user2.id}</code>.",
                parse_mode="HTML",
            )
        else:
            user = await context.bot.get_chat(user_id)
            await update.effective_message.reply_text(
                f"{user.first_name}'s id is <code>{user.id}</code>.", parse_mode="HTML"
            )
    else:
        chat = update.effective_chat
        if chat.type == "private":
            await update.effective_message.reply_text(
                f"Your id is <code>{chat.id}</code>.", parse_mode="HTML"
            )

        else:
            await update.effective_message.reply_text(
                f"This group's id is <code>{chat.id}</code>.", parse_mode="HTML"
            )
