from decouple import config


class EnvironmentSettings:
    def __init__(self):
        self.database = self.load_database()
        self.secret_key = self.load_secret_key()
        self.port = self.load_port()
        self.algorithm = self.load_algorithm()
        self.token_life = self.load_token_expiry()

    def load_database(self):
        return config("DATABASE_URL_FASTAPI")

    def load_secret_key(self):
        return config("SECRET_KEY")

    def load_port(self):
        return config("APP_PORT")

    def load_algorithm(self):
        return config("ALGORITHM")

    def load_token_expiry(self):
        return int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))


variables = EnvironmentSettings()
