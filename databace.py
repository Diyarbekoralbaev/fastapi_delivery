from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://postgres:02052005@localhost/fastapi_learn',echo=True)

Base = declarative_base()
session = sessionmaker()
