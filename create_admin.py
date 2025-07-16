from app.db.database import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        username = "admin"
        email = "admin@example.com"
        full_name = "Admin User"
        password = "admin123"
        hashed_password = get_password_hash(password)

        admin_user = User(
            username=username,
            email=email,
            full_name=full_name,
            password=hashed_password,
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user '{username}' created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
