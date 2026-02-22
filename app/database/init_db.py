from app.database.session import engine, Base
import app.models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco inicializado com sucesso!")

if __name__ == "__main__":
    init_db()