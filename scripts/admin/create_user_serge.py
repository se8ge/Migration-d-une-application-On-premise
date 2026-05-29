import os
import sys
import logging

# Configuration du logging pour voir les erreurs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from app.database import SessionLocal
    from app import models, crud, schemas
    logger.info("Imports réussis")
except Exception as e:
    logger.error(f"Erreur d'import : {e}")
    sys.exit(1)

def create_user_serge():
    db = SessionLocal()
    try:
        email = "sergeanglesy@gmail.com"
        password = "admin123"
        
        logger.info(f"Tentative de création de l'utilisateur : {email}")

        # Vérifier le magasin
        store = db.query(models.Store).first()
        if not store:
            logger.info("Aucun magasin trouvé, création du magasin par défaut...")
            store = models.Store(
                store_name="Magasin Principal", 
                store_code="M01", 
                isactive=True,
                createby="system"
            )
            db.add(store)
            db.commit()
            db.refresh(store)
        
        # Supprimer s'il existe déjà pour repartir propre
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            logger.info("L'utilisateur existe déjà, suppression pour réinitialisation...")
            db.delete(user)
            db.commit()
        
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
        logger.info(f"COMPTE CRÉÉ AVEC SUCCÈS : {new_user.email}")
        
    except Exception as e:
        logger.error(f"ERREUR LORS DE LA CRÉATION : {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_user_serge()
