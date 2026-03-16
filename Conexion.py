from Seguridad import *

connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

def ejecutar_query(self, query: str) -> pd.DataFrame:
    return pd.read_sql(query, self.engine)


