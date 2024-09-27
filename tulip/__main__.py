from telegram.ext import ApplicationBuilder, CommandHandler
from tulip.handlers.misc import start

from tulip import config


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.BOT_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.run_polling()

    bot = application.bot
