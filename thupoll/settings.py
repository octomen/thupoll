import pathlib
from environs import Env


class Environ(Env):
    DEFAULT_DB = 'postgresql://postgres@localhost:5432/postgres'
    DEFAULT_URL = 'http://localhost:5000'
    DEFAULT_TELEGRAM_TOKEN = '123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

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
        return self('BOT_TELEGRAM_TOKEN', self.DEFAULT_TELEGRAM_TOKEN)

    @property
    def bot_proxy_url(self):
        return self('BOT_PROXY_URL', None)

    @property
    def root_path(self):
        return pathlib.Path(__file__).parent.parent

    @property
    def env_path(self):
        return pathlib.Path(__file__).parent


env = Environ()

env.read_env(env.env_path)
