from sqlalchemy import create_engine

from tulip import config

engine = create_engine(config.DB_URI, echo=False)  # echo=True will log all SQL queries
