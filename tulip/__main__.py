from telegram.ext import CommandHandler, MessageHandler
from tulip.handlers.bans import ban, kick, tban, unban
from tulip.handlers.misc import start, id, info
from tulip.handlers.users import log_user

from tulip import LOGGER, application


if __name__ == "__main__":
    # User handlers
    application.add_handler(MessageHandler(None, log_user), group=1)

    # Misc handlers
    application.add_handler(CommandHandler("start", start), group=2)
    application.add_handler(CommandHandler("id", id), group=2)
    application.add_handler(CommandHandler("info", info), group=2)

    # Ban handlers
    application.add_handler(CommandHandler("ban", ban), group=2)
    application.add_handler(CommandHandler("unban", unban), group=2)
    application.add_handler(CommandHandler("kick", kick), group=2)
    application.add_handler(CommandHandler("tban", tban), group=2)

    LOGGER.info("Starting polling...")
    application.run_polling()
