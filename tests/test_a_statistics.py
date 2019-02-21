# coding: utf-8


""" Test for statistics.
"""


__author__ = 'Sidorov D.V.'


import pytest
from models import User, Lecture, db


def test_1(initialize):
    users = [
        {
            'id': 1,
            'name': 'Саша',
            'age': 25
        },
        {
            'id': 2,
            'name': 'Ирина',
            'age': 23
        },
        {
            'id': 3,
            'name': 'Серега',
            'age': 25
        }
    ]
    lectures = [
        {
            'title': 'Шифрование',
            'author': 2,
            'reporter': 2,
            'change_date': '2019-02-21',
            'status': 'create'
        },
        {
            'title': 'Правописание',
            'author': 3,
            'reporter': 1,
            'change_date': '2019-02-21',
            'status': 'create'
        },
        {
            'title': 'Естествознание',
            'author': 1,
            'reporter': 3,
            'change_date': '2019-02-21',
            'status': 'create'
        },
        {
            'title': 'Геология',
            'author': 1,
            'reporter': 1,
            'change_date': '2019-02-21',
            'status': 'create'
        }
    ]

    session = db.session()
    for user in users:
        session.add(User(**user))
        session.commit()

    for lecture in lectures:
        session.add(Lecture(**lecture))
        session.commit()

    _users = session.query(User).all()
    _lectures = session.query(Lecture).all()
    print([user.asdict() for user in _users])
    print([lecture.asdict() for lecture in _lectures])
    session.close()


