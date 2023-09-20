import os


def env(key, type_, default=None):
    if key not in os.environ:
        if default is not None:
            return default
        else:
            raise ValueError(f"Expected environment variable with key {key}")
    val = os.environ[key]

    if type_ == str:
        return str(val)
    elif type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    elif type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None


class _Settings:
    PORT: int = env("PORT", int, 8080)
    PG_DRIVERNAME: str = env("PG_DRIVERNAME", str, 'postgresql+psycopg2')
    PG_HOST: str = env("PG_HOST", str)
    PG_PORT: str = env("PG_PORT", str)
    PG_USERNAME: str = env("PG_USERNAME", str)
    PG_PASSWORD: str = env("PG_PASSWORD", str)
    PG_DATABASE: str = env("PG_DATABASE", str)

    def db_dict(self) -> dict:
        return {
            'drivername': self.PG_DRIVERNAME,
            'host': self.PG_HOST,
            'port': self.PG_PORT,
            'username': self.PG_USERNAME + "asd",
            'password': self.PG_PASSWORD,
            'database': self.PG_DATABASE
        }

    def test_db_dict(self):
        return {
            'drivername': self.PG_DRIVERNAME,
            'host': self.PG_HOST,
            'port': self.PG_PORT,
            'username': self.PG_USERNAME,
            'password': self.PG_PASSWORD,
            'database': f"test_{self.PG_DATABASE}"
        }


SETTINGS = _Settings()
