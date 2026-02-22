from app.database.session import engine, Base
import app.models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("The database has been successfully created.")

if __name__ == "__main__":
    init_db()