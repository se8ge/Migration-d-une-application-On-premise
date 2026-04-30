import os
from app.database import SessionLocal, engine
from app import models, schemas, crud
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

def test_db():
    db = SessionLocal()
    try:

        print("--- Création d'un magasin de test ---")
        store_in = schemas.StoreCreate(
            store_name="Magasin StockLive",
            store_code="T01",
            store_phone="0123456789",
            store_address="123 Rue de Test, Ville",
            createby=" admin"
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
            print("L'utilisateur existe déjà. On l'utilise.")
        else:
            db_user = crud.user_crud.create_user(db, user_in)
            print(f"Utilisateur créé : {db_user.email} (ID: {db_user.id}, StoreID: {db_user.store_id})")


        print("\n--- Vérification de la relation Store -> User ---")
        db_store_refreshed = crud.store_crud.get_store(db, db_store.store_id)
        print(f"Magasin : {db_store_refreshed.store_name}")
        print(f"Utilisateurs rattachés : {[u.email for u in db_store_refreshed.users]}")



    except Exception as e:
        print(f"Erreur durant le test : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_db()
