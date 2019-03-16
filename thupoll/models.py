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

    OCTOPUS = 'octopus'
    INHABITANT = 'inhabitant'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=True, unique=True)


class ThemeStatus(_BaseModel):
    __tablename__ = 'theme_status'

    NEW = 'new'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=True, unique=True)


class People(_BaseModel):
    __tablename__ = 'people'

    id = sa.Column(sa.Integer, primary_key=True)
    role_id = sa.Column(
        sa.Integer, sa.ForeignKey('role.id'), nullable=False)
    telegram_login = sa.Column(sa.String, nullable=False, unique=True)
    created_date = sa.Column(
        sa.DateTime, server_default=sa.func.now(), nullable=False)
    change_date = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
    # relations
    role = relationship(Role)


class Theme(_BaseModel):
    __tablename__ = 'theme'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text)

    author_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'), nullable=False)
    reporter_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'), nullable=False)
    status_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('theme_status.id'),
        nullable=False,
        default=ThemeStatus.NEW,
    )
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
    # relations
    author = relationship(People, foreign_keys=[author_id])
    reporter = relationship(People, foreign_keys=[reporter_id])
    status = relationship(ThemeStatus)


class Poll(_BaseModel):
    __tablename__ = 'poll'

    id = sa.Column(sa.Integer, primary_key=True)
    expire_date = sa.Column(sa.DateTime, nullable=False)
    # TODO poll == meet? or create separate model?
    meet_date = sa.Column(sa.DateTime, nullable=False)
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
    theme_id = sa.Column(sa.Integer, sa.ForeignKey('theme.id'), nullable=False)
    poll_id = sa.Column(sa.Integer, sa.ForeignKey('poll.id'), nullable=False)

    theme = relationship(Theme)
    poll = relationship(Poll)

    __table_args__ = (
        sa.Index(
            'theme_poll_poll_id_theme_id_uidx',
            'poll_id', 'theme_id', unique=True
        ),
    )


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
    themepoll_id = sa.Column(
        sa.Integer, sa.ForeignKey('theme_poll.id'), nullable=False)
    people_id = sa.Column(
        sa.Integer, sa.ForeignKey('people.id'), nullable=False)

    themepoll = relationship(ThemePoll)
    people = relationship(People)

    __table_args__ = (
        sa.Index(
            'volume_people_id_people_id_uidx',
            'people_id', 'themepoll_id', unique=True
        ),
    )
