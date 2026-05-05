import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On lit l'URL depuis l'environnement (Docker) ou on utilise celle par défaut (WAMP local)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost/ghu"
)

# Création de l'engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Si vous voulez garder une trace de l'ancienne config SQLite :
# SQLALCHEMY_DATABASE_URL = "sqlite:///./ghu.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# @event.listens_for(engine, "connect")
# def set_mysql_isolation_level(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
#     cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
