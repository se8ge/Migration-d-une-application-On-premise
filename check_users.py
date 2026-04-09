from app.database import SessionLocal
from app import models

def check_users():
    db = SessionLocal()
    users = db.query(models.User).all()
    print(f"Nombre d'utilisateurs : {len(users)}")
    for user in users:
        print(f"Email: {user.email}, Password ID (hash): {user.password[:20]}...")
    db.close()

if __name__ == "__main__":
    check_users()
