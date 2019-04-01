import factory
import random
from faker import Faker
from thupoll import models


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        models.db.session.add(obj)
        models.db.session.commit()
        return obj


faker = Faker()


def date_between(start, end):
    return factory.LazyFunction(
        lambda: faker.date_between(start_date=start, end_date=end))


def int_between(start, end):
    return factory.LazyFunction(lambda: random.randint(start, end))


class PeopleFactory(BaseFactory):
    class Meta:
        model = models.People

    role_id = models.Role.INHABITANT
    telegram_login = factory.Faker('name')
    name = factory.Faker('name')


class AdminFactory(PeopleFactory):
    role_id = models.Role.OCTOPUS


class ThemeFactory(BaseFactory):
    class Meta:
        model = models.Theme

    title = factory.Faker('name')
    description = factory.Faker('text')
    status_id = models.ThemeStatus.NEW
    author = factory.SubFactory(PeopleFactory)
    reporter = factory.SubFactory(PeopleFactory)


class PollFactory(BaseFactory):
    class Meta:
        model = models.Poll

    expire_date = date_between('+1d', '+3d')
    meet_date = date_between('+3d', '+5d')


class ThemePollFactory(BaseFactory):
    class Meta:
        model = models.ThemePoll

    order_no = int_between(1, 10000)
    theme = factory.SubFactory(ThemeFactory)
    poll = factory.SubFactory(PollFactory)


class Factory:
    people = PeopleFactory
    admin = AdminFactory
    theme = ThemeFactory
    poll = PollFactory
    themepoll = ThemePollFactory
