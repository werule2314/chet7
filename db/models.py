from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

# Связующая таблица: многие ко многим
term_sources = Table(
    'term_sources', Base.metadata,
    Column('term_id', Integer, ForeignKey('terms.id')),
    Column('source_id', Integer, ForeignKey('sources.id'))
)


class Term(Base):
    __tablename__ = 'terms'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    definitions = relationship("Definition", back_populates="term")
    sources = relationship("Source", secondary=term_sources, back_populates="terms")


class Definition(Base):
    __tablename__ = 'definitions'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    term_id = Column(Integer, ForeignKey('terms.id'))
    term = relationship("Term", back_populates="definitions")


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    terms = relationship("Term", secondary=term_sources, back_populates="sources")


def get_engine():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    return create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
