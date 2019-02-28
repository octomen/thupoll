import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DictMixin:
    def asdict(self):
        return {'id': self.id}


class Role(db.Model):
    __tablename__ = 'role'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class ThemeStatus(db.Model):
    __tablename__ = 'theme_status'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class User(db.Model, DictMixin):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_login = sa.Column(sa.String)
    created_date = sa.Column(sa.DateTime, server_default=sa.func.now())
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )


class Theme(db.Model, DictMixin):

    __tablename__ = 'theme'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    author_id = sa.Column(sa.Integer)
    reporter_id = sa.Column(sa.Integer)
    status_id = sa.Column(sa.Integer)
    created_date = sa.Column(sa.DateTime, server_default=sa.func.now())
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    author = relationship(User, back_populates="author")
    reporter = relationship(User, back_populates="reporter")
    status = relationship(ThemeStatus, back_populates="status")


class Poll(db.Model):
    __tablename__ = 'poll'

    id = sa.Column(sa.Integer, primary_key=True)
    expire_date = sa.Column(sa.DateTime)
    created_date = sa.Column(sa.DateTime, server_default=sa.func.now())
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )


class ThemePoll(db.Model):
    __tablename__ = 'theme_poll'

    id = sa.Column(sa.Integer, primary_key=True)
    theme_id = sa.Column(sa.Integer)
    poll_id = sa.Column(sa.Integer)

    themes = relationship(Theme, back_populates="themes")
    polls = relationship(Poll, back_populates="polls")


class Volume(db.Model):
    __tablename__ = 'volume'

    id = sa.Column(sa.Integer, primary_key=True)

    created_date = sa.Column(sa.DateTime, server_default=sa.func.now())
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    themepoll_id = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer)

    themepoll = relationship(ThemePoll, back_populates="themepoll")
    user = relationship(User, back_populates="user")
