from sqlalchemy import create_engine
from models import Base

ENGINE_URL = "postgresql://user:password@target_db:5432/target_db"
engine = create_engine(ENGINE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tabelas criadas em target_db")
