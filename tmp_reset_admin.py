from app.database import SessionLocal
from app import models, crud, schemas
from sqlalchemy.orm import Session

def reset_admin():
    db = SessionLocal()
    email = "admin@test.com"
    password = "admin"
    
    # Supprimer l'ancien s'il existe
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
    
    # Créer un magasin par défaut s'il n.y en a pas
    store = db.query(models.Store).first()
    if not store:
        store = models.Store(store_name="Magasin Principal", store_code="M01", isactive=True)
        db.add(store)
        db.commit()
        db.refresh(store)
    
    # Créer l'utilisateur
    user_in = schemas.UserCreate(
        email=email,
        firstname="Admin",
        lastname="Test",
        password=password,
        is_admin=True,
        store_id=store.store_id
    )
    new_user = crud.user_crud.create_user(db, user_in)
    print(f"Utilisateur créé avec succès : {new_user.email} / mot de passe: {password}")
    db.close()

if __name__ == "__main__":
    reset_admin()
