from urllib.parse import urlunparse, urlencode

from thupoll.settings import env


class FrontUrl:
    SCHEME = "https"
    HOSTNAME = env.thupoll_url

    @classmethod
    def urlunparse(cls, path, **kw):
        return urlunparse((
            cls.SCHEME, cls.HOSTNAME, path, None, urlencode(kw), ""))

    @classmethod
    def poll(cls, poll_id):
        return cls.urlunparse("/poll", poll_id=poll_id)

    @classmethod
    def login(cls, token):
        return cls.urlunparse("/login", token=token)
