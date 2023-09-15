import os

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': 'localhost',
    'port': '5432',
    'username': 'denis',
    'password': 'localpass',
    'database': 'python_messenger'
}


def env(key, type_, default=None):
    if key not in os.environ:
        if default is not None:
            return default
        else:
            raise ValueError(f"Expected environment variable with key {key}")
    val = os.environ[key]

    if type_ == str:
        return val
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


SETTINGS = _Settings()
