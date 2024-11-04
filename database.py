from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import URL_DATABASE # url to connect to ur database : create settings.py file and put the URL_DATABASE(string) var there




engine = create_engine(URL_DATABASE)

SessonLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
