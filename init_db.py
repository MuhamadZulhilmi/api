from app.db import database

def init_db():
    # Importing database module will trigger Base.metadata.create_all(engine)
    pass

if __name__ == "__main__":
    init_db()
    print("Database schema initialized successfully.")
