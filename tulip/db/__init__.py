from tulip import config
from sqlalchemy import create_engine

engine = create_engine(config.DB_URI, echo=True)  # echo=True will log all SQL queries
