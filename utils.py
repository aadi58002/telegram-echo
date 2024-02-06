import os

def get_env(var_name: str) -> str:
    try:
        val = os.environ[var_name]
    except KeyError:
        raise Exception("Telegram {var_name} not found in environment variables.")

    return str(val)
