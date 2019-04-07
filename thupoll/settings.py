import pathlib
from environs import Env


class Environ(Env):
    DEFAULT_DB = 'postgresql://postgres@localhost:5432/postgres'
    DEFAULT_URL = 'http://localhost:5000'
    DEFAULT_TELEGRAM_TOKEN = '123456789:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    def __init__(self):
        super(Environ, self).__init__()
        chats = self('MONITORED_CHATS', None)
        self.__chats = {int(i) for i in chats.split(',')} if chats else set()

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

    @property
    def monitored_chats(self):
        return self.__chats


env = Environ()

env.read_env(env.env_path)
