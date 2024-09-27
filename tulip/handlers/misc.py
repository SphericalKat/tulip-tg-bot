from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm Tulip - A bot to help manage your groups! Use the /help command to see what I can do!",
    )

async def id()