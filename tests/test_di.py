import pytest

from thupoll.utils import di


def provider(a, b):
    return a+b


params = pytest.mark.parametrize("factory_class", [di.Factory, di.Singleton])


@params
def test__simple_run(factory_class, faker):
    x, y = faker.pyint(), faker.pyint()
    factory = factory_class(provider, a=x, b=y)
    assert factory() == x+y


@params
def test__override_kw(factory_class, faker):
    x, y = faker.pyint(), faker.pyint()
    factory = factory_class(provider, a=y)
    assert factory(a=x, b=y) == x+y


@params
def test__override_factory(factory_class, faker):
    x, y, z = faker.pyint(), faker.pyint(), faker.pyint()
    factory = factory_class(provider, a=x, b=x)
    factory.override(factory_class(provider, a=y, b=y))
    factory.override(factory_class(provider, a=z, b=z))
    assert factory(b=x) == z+x
    factory.reset()
    assert factory() == y+y


def test__singleton(faker):
    x, y = faker.pyint(), faker.pyint()
    factory = di.Singleton(provider)
    assert factory(a=x, b=x) == factory(a=y, b=y)


@params
def test__dependencies(factory_class, faker):
    x, y = faker.pyint(), faker.pyint()
    child_factory = factory_class(provider, a=x, b=x)
    parent_factory = factory_class(provider, a=y, b=child_factory)
    assert parent_factory() == x+x+y


# def test__container(faker)
