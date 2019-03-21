import datetime

from thupoll import models as m
from thupoll.blueprints.telegram.error import BotAuthException


class AuthAdapter:
    """Authorization logic"""
    def __init__(self, session, token_ttl_days):
        self.session = session
        self.token_ttl_days = token_ttl_days

    def exist_user(self, identifier):
        """Check existence user in database by identifier"""
        query = self.session.query(
            m.People
        ).filter(
            m.People.telegram_login == str(identifier)
        ).exists()

        query = self.session.query(query)

        return query.scalar()

    def generate_token(self, identifier):
        """Generate user token in database by identifier"""
        people = self.session.query(
            m.People
        ).filter(
            m.People.telegram_login == str(identifier)
        ).one_or_none()

        if people is None:
            raise BotAuthException(
                "People wiht identifier = {} "
                "does not exist".format(identifier))
        token = m.Token(
            people=people,
            expire=(datetime.datetime.now() +
                    datetime.timedelta(days=int(self.token_ttl_days)))
        )
        self.session.add(token)
        self.session.flush()
        return token.value
