import factory
import random
import string
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


def strand(length=40):
    return factory.LazyFunction(
        lambda: ''.join(
            random.choice(string.ascii_lowercase) for i in range(length)
        ))


class SessionFactory(BaseFactory):
    class Meta:
        model = models.Session

    people = factory.SubFactory('tests.factories.PeopleFactory')
    value = strand(40)


class PeopleFactory(BaseFactory):
    class Meta:
        model = models.People

    role_id = models.Role.INHABITANT
    telegram_login = factory.Faker('name')
    name = factory.Faker('name')
    session = factory.RelatedFactory(SessionFactory, 'people')


class AdminFactory(PeopleFactory):
    role_id = models.Role.OCTOPUS


class NamespaceFactory(BaseFactory):
    class Meta:
        model = models.Namespace

    code = factory.Faker('text')
    name = factory.Faker('text')
    telegram_chat_id = int_between(0, 10000)


class PeopleNamespaceFactory(BaseFactory):
    class Meta:
        model = models.PeopleNamespace

    role_id = models.Role.INHABITANT
    people = factory.SubFactory(PeopleFactory)
    namespace = factory.SubFactory(NamespaceFactory)


class ThemeFactory(BaseFactory):
    class Meta:
        model = models.Theme

    title = factory.Faker('name')
    description = factory.Faker('text')
    status_id = models.ThemeStatus.NEW
    author = factory.SubFactory(PeopleFactory)
    reporter = factory.SubFactory(PeopleFactory)
    namespace = factory.SubFactory(NamespaceFactory)


class PollFactory(BaseFactory):
    class Meta:
        model = models.Poll

    expire_date = date_between('+1d', '+3d')
    meet_date = date_between('+3d', '+5d')
    namespace = factory.SubFactory(NamespaceFactory)


class ThemePollFactory(BaseFactory):
    class Meta:
        model = models.ThemePoll

    order_no = int_between(1, 10000)
    theme = factory.SubFactory(ThemeFactory)
    poll = factory.SubFactory(PollFactory)


def authheader_factory(people):
    # TODO create session if not exists ?
    return {'Authentication': people.sessions[0].value}


class Factory:
    people = PeopleFactory
    admin = AdminFactory
    theme = ThemeFactory
    poll = PollFactory
    themepoll = ThemePollFactory
    namespace = NamespaceFactory
    peoplenamespace = PeopleNamespaceFactory
    authheader = authheader_factory
