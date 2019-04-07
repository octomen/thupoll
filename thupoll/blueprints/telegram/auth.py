import datetime

from thupoll import models as m
from thupoll.blueprints.telegram.error import BotAuthException


class AuthAdapter:
    def __init__(self, session):
        self.session = session

    def exist_user(self, identifier):
        """Check existence user in database by identifier"""
        query = self.session.query(
            m.People
        ).filter(
            m.People.telegram_login == str(identifier)
        ).exists()

        query = self.session.query(query)

        return query.scalar()


class RegistrationAdapter(AuthAdapter):
    def create_inhabitant(self, name: str, telegram_login: str) -> m.People:
        people = m.People(
            name=name, telegram_login=telegram_login,
            role_id=m.Role.INHABITANT,
        )
        self.session.add(people)
        return people


class TokenAdapter(AuthAdapter):
    def __init__(self, session, token_ttl_days):
        super(TokenAdapter, self).__init__(session=session)
        self.token_ttl_days = token_ttl_days

    def generate_token(self, identifier):
        """Generate user token in database by identifier"""
        people = self.session.query(
            m.People
        ).filter(
            m.People.telegram_login == str(identifier)
        ).one_or_none()

        if people is None:
            raise BotAuthException(
                "People with identifier = {} "
                "does not exist".format(identifier))
        # invalidate old tokens
        self.session.query(m.Token).filter(
            m.Token.people_id == people.id).delete()
        # create new token
        token = m.Token(
            people=people,
            expire=(datetime.datetime.now() +
                    datetime.timedelta(days=int(self.token_ttl_days)))
        )
        self.session.add(token)
        self.session.flush()
        return token.value
