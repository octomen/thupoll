import typing
from thupoll import models


def __query(people: models.People):
    q = models.db.session.query(
        models.PeopleNamespace
    )
    if people.role_id != models.Role.OCTOPUS:
        q = q.filter_by(people_id=people.id)
    return q


def all(people: models.People) -> typing.List[models.PeopleNamespace]:
    return __query(people).all()


def get(
        people: models.People,
        code: str,
) -> typing.Optional[models.PeopleNamespace]:
    return __query(people).filter_by(namespace_code=code).one_or_none()
