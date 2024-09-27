import logging
from tulip.config import Config
from telegram.ext import ApplicationBuilder


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

LOGGER.addHandler(handler)

LOGGER.propagate = False

LOGGER.info("Logger initialized.")

config = Config()

application = ApplicationBuilder().token(config.BOT_API_TOKEN).build()
bot = application.bot