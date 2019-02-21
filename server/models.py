# coding: utf-8


import psycopg2
import psycopg2.extras
from psycopg2 import connect
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
from config import DATABASE


Base = declarative_base()


def get_session():
    engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % (
        DATABASE['user'],
        DATABASE['password'],
        DATABASE['host'],
        DATABASE['port'],
        DATABASE['dbname']
    ), echo=False)
    return Session(bind=engine, autoflush=False)


def get_conn():
    return connect(
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port'],
        dbname=DATABASE['dbname']
    )


class PsqlDriver(object):

    def __init__(self):
        self.connection = \
            psycopg2.connect(**DATABASE)

    def __enter__(self):
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return self.cursor

    def __exit__(self, type, value, tb):
        if tb is None:
            self.connection.commit()
            self.cursor.close()
        else:
            self.connection.rollback()


lecture_status = ENUM('create', 'preparing', 'planning', 'discarded', 'done', name='lecture_status')


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


class Lecture(Base):

    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    author = Column(Integer, ForeignKey(User))
    reporter = Column(Integer, ForeignKey(User))
    change_date = Column(Date)
    status = Column(lecture_status)
