import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

#Connection to database in Postgre SQL

DB_NAME = os.environ.get("DB_NAME", "testdb")

engine = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{DB_NAME}"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
