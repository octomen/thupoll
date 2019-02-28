import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class _BaseModel(db.Model):
    __abstract__ = True

    def asdict(self):  # TODO выпилить это
        return {'id': self.id}


class Role(_BaseModel):
    __tablename__ = 'role'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class ThemeStatus(_BaseModel):
    __tablename__ = 'theme_status'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class User(_BaseModel):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_login = sa.Column(sa.String, nullable=False)
    created_date = sa.Column(
        sa.DateTime, server_default=sa.func.now(), nullable=False)
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )


class Theme(_BaseModel):

    __tablename__ = 'theme'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text)
    author_id = sa.Column(sa.Integer, nullable=False)
    reporter_id = sa.Column(sa.Integer, nullable=False)
    status_id = sa.Column(sa.Integer, nullable=False)
    created_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    author = relationship(User, back_populates="author")
    reporter = relationship(User, back_populates="reporter")
    status = relationship(ThemeStatus, back_populates="status")


class Poll(_BaseModel):
    __tablename__ = 'poll'

    id = sa.Column(sa.Integer, primary_key=True)
    expire_date = sa.Column(sa.DateTime, nullable=False)
    created_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )


class ThemePoll(_BaseModel):
    __tablename__ = 'theme_poll'

    id = sa.Column(sa.Integer, primary_key=True)
    theme_id = sa.Column(sa.Integer, nullable=False,)
    poll_id = sa.Column(sa.Integer, nullable=False,)

    themes = relationship(Theme, back_populates="themes")
    polls = relationship(Poll, back_populates="polls")


class Volume(_BaseModel):
    __tablename__ = 'volume'

    id = sa.Column(sa.Integer, primary_key=True)

    created_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    themepoll_id = sa.Column(sa.Integer, nullable=False,)
    user_id = sa.Column(sa.Integer, nullable=False,)

    themepoll = relationship(ThemePoll, back_populates="themepoll")
    user = relationship(User, back_populates="user")
