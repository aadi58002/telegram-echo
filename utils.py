import os

def getEnv(var_name: str) -> str:
    try:
        val = os.environ[var_name]
    except KeyError:
        raise Exception(f"Telegram {var_name} not found in environment variables.")

    return str(val)
