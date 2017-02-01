
from sqlalchemy import create_engine

def get_engine():
    engine = create_engine('mysql+pymysql://user:pass@localhost:3306/dbname')
    return engine

