from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

lecture_status = ENUM(
    'create', 'preparing', 'planning', 'discarded', 'done',
    name='lecture_status',
)


class DictMixin:

    def asdict(self):
        return self._asdict()


class User(db.Model, DictMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


class Lecture(db.Model, DictMixin):

    __tablename__ = 'lecture'

    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    author = Column(Integer, ForeignKey('user.id'))
    reporter = Column(Integer, ForeignKey('user.id'))
    change_date = Column(Date)
    status = Column(lecture_status)
