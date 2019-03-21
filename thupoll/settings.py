from environs import Env


class Environ(Env):
    DEFAULT_DB = 'postgresql://postgres@localhost:5432/postgres'
    DEFAULT_URL = 'http://localhost:5000'

    @property
    def db_url(self):
        return self('DB_URL', self.DEFAULT_DB)

    @property
    def thupoll_url(self):
        return self("THUPOLL_URL", self.DEFAULT_URL)

    @property
    def log_level(self):
        return self('LOG_LEVEL', 'INFO')

    @property
    def bot_telegram_token(self):
        return self('BOT_TELEGRAM_TOKEN', validate=lambda x: bool(x))

    @property
    def bot_proxy_url(self):
        return self('BOT_PROXY_URL', None)


env = Environ()

env.read_env()
