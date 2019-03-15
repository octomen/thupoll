import pytest

from thupoll import models


@pytest.mark.parametrize('model', [
    models.People,
    models.Role,
    models.ThemeStatus,
    models.People,
    models.Theme,
    models.Poll,
    models.ThemePoll,
    models.Volume,
])
def test_correct_simple_select(model, db_session):
    db_session.query(model).all()
