import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


freeze_tables = {'role', 'theme_status'}


class _BaseModel(db.Model):
    __abstract__ = True

    def marshall(self) -> dict:
        raise NotImplementedError


class Role(_BaseModel):
    __tablename__ = 'role'

    OCTOPUS = 1
    INHABITANT = 2

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=True, unique=True)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
        )


class ThemeStatus(_BaseModel):
    __tablename__ = 'theme_status'

    NEW = 1

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=True, unique=True)

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
        )


class People(_BaseModel):
    __tablename__ = 'people'

    id = sa.Column(sa.Integer, primary_key=True)
    role_id = sa.Column(
        sa.Integer, sa.ForeignKey('role.id'), nullable=False)
    telegram_login = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    created_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
    # relations
    role = relationship(Role, lazy='joined')  # type: Role

    def is_admin(self):
        return self.role_id == Role.OCTOPUS

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            role_id=self.role_id,
            name=self.name,
            telegram=self.telegram_login,
            created=self.created_date,
            updated=self.change_date,
        )


class Theme(_BaseModel):
    __tablename__ = 'theme'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text)

    author_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'), nullable=False)
    reporter_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'))
    status_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('theme_status.id'),
        nullable=False,
        default=ThemeStatus.NEW,
    )
    created_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
    # relations
    author = relationship(
        People, foreign_keys=[author_id], lazy='joined')  # type: People
    reporter = relationship(
        People, foreign_keys=[reporter_id], lazy='joined')  # type: People
    status = relationship(ThemeStatus, lazy='joined')  # type: ThemeStatus
    polls = relationship(
        "Poll", secondary="theme_poll", back_populates="themes")

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            author=self.author.marshall(),
            reporter=self.reporter.marshall() if self.reporter else {},
            status=self.status.marshall(),
            created=self.created_date,
            updated=self.change_date,
        )


class Poll(_BaseModel):
    __tablename__ = 'poll'

    id = sa.Column(sa.Integer, primary_key=True)
    expire_date = sa.Column(sa.DateTime, nullable=False)
    # TODO poll == meet? or create separate model?
    meet_date = sa.Column(sa.DateTime, nullable=False)
    created_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
    themes = relationship(
        "Theme",
        secondary="theme_poll",
        back_populates="polls"
    )

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            expire_date=self.expire_date,
            meet_date=self.meet_date,
            created=self.created_date,
            updated=self.change_date,
        )


class ThemePoll(_BaseModel):
    __tablename__ = 'theme_poll'

    id = sa.Column(sa.Integer, primary_key=True)
    theme_id = sa.Column(sa.Integer, sa.ForeignKey('theme.id'), nullable=False)
    poll_id = sa.Column(sa.Integer, sa.ForeignKey('poll.id'), nullable=False)

    theme = relationship(Theme, lazy='joined')  # type: Theme
    poll = relationship(Poll, lazy='joined')  # type: Poll

    __table_args__ = (
        sa.Index(
            'theme_poll_poll_id_theme_id_uidx',
            'poll_id', 'theme_id', unique=True
        ),
    )

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            theme=self.theme.marshall(),
            poll=self.poll.marshall(),
        )


class Volume(_BaseModel):
    __tablename__ = 'volume'

    id = sa.Column(sa.Integer, primary_key=True)

    created_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
    change_date = sa.Column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    themepoll_id = sa.Column(
        sa.Integer, sa.ForeignKey('theme_poll.id'), nullable=False)
    people_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'), nullable=False)

    themepoll = relationship(ThemePoll, lazy='joined')  # type: ThemePoll
    people = relationship(People, lazy='joined')  # type: People

    __table_args__ = (
        sa.Index(
            'volume_people_id_people_id_uidx',
            'people_id', 'themepoll_id', unique=True
        ),
    )

    def marshall(self) -> dict:
        return dict(
            id=self.id,
            theme=self.theme.marshall(),
            poll=self.poll.marshall(),
            themepoll=self.themepoll.marshall(),
            people=self.people.marshall(),
        )


class Token(_BaseModel):
    __tablename__ = "token"

    id = sa.Column(sa.Integer, primary_key=True)
    people_id = sa.Column(
        sa.Integer, sa.ForeignKey("people.id"), nullable=False)
    value = sa.Column(
        sa.String,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    expire = sa.Column(sa.DateTime, nullable=False)

    people = relationship(People, lazy='joined')  # type: People


class Session(_BaseModel):
    __tablename__ = "session"

    id = sa.Column(sa.Integer, primary_key=True)
    people_id = sa.Column(
        sa.Integer, sa.ForeignKey("people.id"), nullable=False)
    value = sa.Column(
        sa.String,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        unique=True,
    )
    expire = sa.Column(sa.DateTime)

    people = relationship(People, lazy='joined')  # type: People
