from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///../MyExpenseDatabase"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

LocalSession=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

Base=declarative_base()