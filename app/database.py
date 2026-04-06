from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On utilise la base 'ghu' existante de Laragon pour commencer
SQLALCHEMY_DATABASE_URL = "sqlite:///./ghu.db"

# Pour SQLite, nous avons besoin de connect_args={"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Désactivé pour SQLite
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
