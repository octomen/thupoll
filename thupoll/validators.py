from thupoll import models

from marshmallow.exceptions import ValidationError


# TODO remove copypasting


def people_id(
        value: int,
        must_exists: bool,
):
    if not value:
        return
    obj = models.db.session.query(models.People).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'People', 'id={}'.format(value), must_exists=must_exists))


def theme_status_id(
        value: int,
        must_exists: bool,
):
    if not value:
        return
    obj = models.db.session.query(models.ThemeStatus).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'ThemeStatus', 'id={}'.format(value), must_exists=must_exists))


def theme_id(
        value: int,
        must_exists: bool,
):
    if not value:
        return
    obj = models.db.session.query(models.Theme).get(value)
    if must_exists == bool(obj):
        return obj
    raise ValidationError(__exists_error_message(
        'Theme', 'id={}'.format(value), must_exists=must_exists))


def __exists_error_message(name, key, must_exists):
    if must_exists:
        return '{name} with {key} does not exists'.format(name=name, key=key)
    return '{name} with {key} already exists'.format(name=name, key=key)