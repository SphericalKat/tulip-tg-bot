from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from tulip.handlers.misc import start
from tulip.handlers.users import log_user

from tulip import config


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.BOT_API_TOKEN).build()

    application.add_handler(MessageHandler(None, log_user), group=1)
    application.add_handler(CommandHandler("start", start), group=2)
    application.run_polling()

    bot = application.bot
