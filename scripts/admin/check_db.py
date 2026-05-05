import os
import sys

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine, inspect
from app.database import SQLALCHEMY_DATABASE_URL

def check_db():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Connexion réussie à : {SQLALCHEMY_DATABASE_URL}")
        print(f"Tables trouvées ({len(tables)}) : {', '.join(tables)}")
        
        with engine.connect() as conn:
            for table in tables:
                res = conn.execute(f"SELECT COUNT(*) FROM {table}")
                count = res.fetchone()[0]
                print(f" - Table {table}: {count} lignes")
                
    except Exception as e:
        print(f"ERREUR : Impossible de se connecter à la base de données : {e}")

if __name__ == "__main__":
    check_db()
