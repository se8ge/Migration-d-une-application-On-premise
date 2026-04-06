from sqlalchemy import text
from app import database, models, crud

def fix_password_column():
    db = next(database.get_db())
    try:
        # Modifier la taille de la colonne pour accueillir le hash
        db.execute(text("ALTER TABLE `user` MODIFY password VARCHAR(255);"))
        db.commit()
        print("Colonne password agrandie à VARCHAR(255).")
        
        # Réinitialiser le mot de passe de admin@admin.com
        user = crud.user_crud.get_user_by_email(db, "admin@admin.com")
        if user:
            user.password = crud.pwd_context.hash("admin123")
            db.commit()
            print("Mot de passe mis à jour pour admin@admin.com avec succès: admin123")
        else:
            print("Utilisateur introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    fix_password_column()
