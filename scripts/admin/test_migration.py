import os
from app.database import SessionLocal, engine
from app import models, schemas, crud
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

def test_db():
    db = SessionLocal()
    try:
        print("--- Vérification de la connexion ---")
        # Test simple de connexion
        db.execute("SELECT 1")
        print("Connexion réussie !")

        print("\n--- Création des tables ---")
        models.Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès.")

        print("\n--- Création d'un magasin de test ---")
        store_in = schemas.StoreCreate(
            store_name="Magasin StockLive",
            store_code="T01",
            store_phone="0123456789",
            store_address="123 Rue de Test, Ville",
            createby="admin"
        )
        db_store = crud.store_crud.create_store(db, store_in)
        print(f"Magasin créé : {db_store.store_name} (ID: {db_store.store_id})")

        print("\n--- Création d'un utilisateur de test lié au magasin ---")
        user_in = schemas.UserCreate(
            email="test_user_store@example.com",
            firstname="Test",
            lastname="User",
            password="password123",
            is_admin=False,
            store_id=db_store.store_id
        )
        db_user = crud.user_crud.get_user_by_email(db, email=user_in.email)
        if db_user:
            print("L'utilisateur existe déjà.")
        else:
            db_user = crud.user_crud.create_user(db, user_in)
            print(f"Utilisateur créé : {db_user.email} (ID: {db_user.id})")

        print("\n--- Vérification de la relation Store -> User ---")
        db_store_refreshed = crud.store_crud.get_store(db, db_store.store_id)
        print(f"Magasin : {db_store_refreshed.store_name}")
        users = [u.email for u in db_store_refreshed.users]
        print(f"Utilisateurs rattachés : {users}")
        
        if db_user.email not in users:
            raise Exception("L'utilisateur n'est pas rattaché au magasin !")

        print("\n✅ TEST RÉUSSI !")

    except Exception as e:
        print(f"\n❌ ERREUR DURANT LE TEST : {e}")
        db.rollback()
        raise e # On relance l'erreur pour que le CI/CD échoue proprement avec un message
    finally:
        db.close()

if __name__ == "__main__":
    test_db()
