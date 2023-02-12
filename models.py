from sqlalchemy import Column, DateTime, Integer, String, create_engine, func, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import atexit


PG_DSN = 'postgresql://postgres:1234@127.0.0.1:5431/roman_ads'
engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class User(Base):
    __tablename__ = 'ads_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Post(Base):

    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True)
    description = Column(Text)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, ForeignKey(User.username))


Base.metadata.create_all(bind=engine)