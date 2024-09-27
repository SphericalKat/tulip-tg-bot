import logging
from sqlalchemy import create_engine
from tulip.config import Config


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

config = Config()

engine = create_engine(config.DB_URI, echo=True) # echo=True will log all SQL queries
