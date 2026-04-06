from sqlalchemy.orm import Session
from app import models, database, crud
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def check_users():
    db = next(database.get_db())
    users = db.query(models.User).all()
    print(f"Nombre d'utilisateurs: {len(users)}")
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, Admin: {user.is_admin}")
    
    # Créer un utilisateur admin de test si aucun n'existe
    if not users:
        admin_user = models.User(
            email="admin@example.com",
            firstname="Admin",
            lastname="System",
            password=pwd_context.hash("admin123"),
            is_admin=True,
            status=1
        )
        db.add(admin_user)
        db.commit()
        print("Utilisateur admin créé: admin@example.com / admin123")

if __name__ == "__main__":
    check_users()
