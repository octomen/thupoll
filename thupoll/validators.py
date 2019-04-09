from datetime import datetime
from flask import abort, g
from marshmallow.exceptions import ValidationError
from typing import Iterator, Optional as Op

from thupoll import models
from thupoll.utils import assert_auth


# TODO remove copypasting


def people_id(
        value: int,
        must_exists: bool = True,
) -> Op[models.People]:
    if not value:
        return
    obj = models.db.session.query(models.People).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'People', 'id={}'.format(value), must_exists=must_exists))


def theme_status_id(
        value: int,
        must_exists: bool = True,
) -> Op[models.ThemeStatus]:
    if not value:
        return
    obj = models.db.session.query(models.ThemeStatus).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'ThemeStatus', 'id={}'.format(value), must_exists=must_exists))


def theme_id(
        value: int,
        must_exists: bool = True,
) -> Op[models.Theme]:
    if not value:
        return
    obj = models.db.session.query(models.Theme).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'Theme', 'id={}'.format(value), must_exists=must_exists))


def poll_id(
        value: int,
        must_exists: bool = True,
) -> Op[models.Poll]:
    if not value:
        return
    obj = models.db.session.query(models.Poll).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'Poll', 'id={}'.format(value), must_exists=must_exists))


def themepoll(
        theme_id: int,
        poll_id: int,
        must_exists: bool = True,
) -> Op[models.ThemePoll]:
    obj = models.db.session.query(
        models.ThemePoll
    ).filter_by(
        theme_id=theme_id,
        poll_id=poll_id,
    ).one_or_none()
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'ThemePoll', 'poll_id={} theme_id={}'.format(
            poll_id, theme_id), must_exists=must_exists))


def __exists_error_message(name, key, must_exists):
    if must_exists:
        return '{name} with {key} does not exists'.format(name=name, key=key)
    return '{name} with {key} already exists'.format(name=name, key=key)


def future_datetime_validator(date: datetime):
    if datetime.now() > date:
        raise ValidationError('Datetime {} from past'.format(date))


def distinct(iterable: Iterator, name, fetcher=lambda x: x):
    if len(set(map(fetcher, iterable))) != len(iterable):
        raise ValidationError('Duplication values of {}'.format(name))


def dataful(seq_name: str, sequence: Iterator):
    if len(sequence) == 0:
        raise ValidationError("Sequence {!r} is empty".format(seq_name))


def namespace_code(
        value: str,
        must_exists: bool,
) -> Op[models.Namespace]:
    if not value:
        return
    obj = models.db.session.query(models.Namespace).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'Namespace', 'code={}'.format(value), must_exists=must_exists))


def namespace_access(
        code: str,
        admin: bool = False,
) -> models.Namespace:
    # check auth
    assert_auth()
    # find session
    namespace = namespace_code(code, must_exists=True)
    # check permissions
    if g.people.role_id != models.Role.OCTOPUS:
        people_namespace = models.db.session.query(
            models.PeopleNamespace
        ).filter_by(
            people_id=g.people.id,
            namespace_code=namespace.code,
        ).one_or_abort(403)  # type: models.PeopleNamespace
        # if needed admin permissions to namespace
        if admin and people_namespace.role_id != models.Role.OCTOPUS:
            abort(403)
    return namespace
