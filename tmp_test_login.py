from app import database, models, crud

def test_login():
    db = next(database.get_db())
    user = crud.user_crud.get_user_by_email(db, "admin@admin.com")
    print(f"User found: {user is not None}")
    if user:
        print(f"Hash in DB: {user.password}")
        is_valid = crud.pwd_context.verify("admin123", user.password)
        print(f"Password valid: {is_valid}")

if __name__ == "__main__":
    test_login()
