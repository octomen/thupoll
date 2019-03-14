from environs import Env


class Environ(Env):
    DEFAULT_DB = 'postgresql://postgres@localhost:5432/postgres'

    @property
    def db_url(self):
        return self('DB_URL', self.DEFAULT_DB)

    @property
    def test_db_url(self):
        return self('TEST_DB_URL', self.DEFAULT_DB)

    @property
    def log_level(self):
        return self('LOG_LEVEL', 'INFO')


env = Environ()
