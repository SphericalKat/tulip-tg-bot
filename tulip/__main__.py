from telegram.ext import CommandHandler, MessageHandler

from tulip import LOGGER, application
from tulip.handlers.admin import demote, promote
from tulip.handlers.bans import ban, kick, tban, unban
from tulip.handlers.misc import id, info, start
from tulip.handlers.mute import mute, tmute, unmute
from tulip.handlers.users import log_user

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

    # mute handlers
    application.add_handler(CommandHandler("mute", mute), group=2)
    application.add_handler(CommandHandler("unmute", unmute), group=2)
    application.add_handler(CommandHandler("tmute", tmute), group=2)

    # admin handlers
    application.add_handler(CommandHandler("promote", promote), group=2)
    application.add_handler(CommandHandler("demote", demote), group=2)

    LOGGER.info("Starting polling...")
    application.run_polling()
