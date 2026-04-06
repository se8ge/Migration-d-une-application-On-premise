from sqlalchemy.orm import Session
from app import models, database, crud
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def reset_admin():
    db = next(database.get_db())
    user = db.query(models.User).filter(models.User.email == "admin@admin.com").first()
    if user:
        user.password = pwd_context.hash("admin123")
        db.commit()
        print("Mot de passe mis à jour pour admin@admin.com: admin123")
    else:
        print("Utilisateur non trouvé.")

if __name__ == "__main__":
    reset_admin()
