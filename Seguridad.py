from Entradas import *

ruta_env = os.path.expanduser("~/Desktop/.env")
load_dotenv(dotenv_path=ruta_env)

def get_env_variable(nombre: str, default=None):
    return os.getenv(nombre, default)

user = quote_plus(get_env_variable("NAME"))
password = quote_plus(get_env_variable("SQL_PASSWORD"))
host = get_env_variable("SQL_HOST")
port =  "3306"
database = get_env_variable("SQL_DB")


