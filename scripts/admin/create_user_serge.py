import os
import sys

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal
from app import models, crud, schemas

def create_user_serge():
    db = SessionLocal()
    email = "sergeanglesy@gmail.com"
    password = "admin123"
    
    # Supprimer s'il existe déjà pour repartir propre
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
    
    # Vérifier le magasin
    store = db.query(models.Store).first()
    if not store:
        store = models.Store(store_name="Magasin Principal", store_code="M01", isactive=True)
        db.add(store)
        db.commit()
        db.refresh(store)
    
    # Créer l'utilisateur Serge
    user_in = schemas.UserCreate(
        email=email,
        firstname="Serge",
        lastname="Anglesy",
        password=password,
        is_admin=True,
        store_id=store.store_id
    )
    new_user = crud.user_crud.create_user(db, user_in)
    print(f"COMPTE CRÉÉ : {new_user.email}")
    print(f"MOT DE PASSE : {password}")
    db.close()

if __name__ == "__main__":
    create_user_serge()
