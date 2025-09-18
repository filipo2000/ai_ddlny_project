import os
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from db import SessionLocal , metadata , engine
# Load environment variables from .env file
load_dotenv()


#Tests connection to database in Postgre SQL

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

# Step 1: Connect to default "postgres" database to create DB if it doesn't exist
default_engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
)

try:
    with default_engine.connect() as conn:
        conn.execute(text(f"COMMIT"))  # Ensure autocommit
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
        print(f"✅ Database '{DB_NAME}' created successfully!")
except ProgrammingError as e:
    if f'database "{DB_NAME}" already exists' in str(e):
        print(f"ℹ️ Database '{DB_NAME}' already exists.")
    else:
        raise e

# Step 2: Connect to the target database
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Base = declarative_base()

# Step 3: Define tables
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    stock = Column(Integer)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)

# Step 4: Create tables
Base.metadata.create_all(engine)
print("✅ Tables created successfully!")

# Step 5: Insert sample data
Session = sessionmaker(bind=engine)
session = Session()

# Check if tables already have data
if not session.query(Product).first():
    products = [
        Product(name="Widget A", price=19.99, stock=100),
        Product(name="Widget B", price=29.99, stock=50),
        Product(name="Widget C", price=9.99, stock=200)
    ]
    session.add_all(products)

if not session.query(Customer).first():
    customers = [
        Customer(name="Alice", email="alice@example.com"),
        Customer(name="Bob", email="bob@example.com")
    ]
    session.add_all(customers)

session.commit()
print("✅ Sample data inserted!")

# Step 6: Test a query
result = session.execute(text("SELECT * FROM products LIMIT 5"))
for row in result:
    print(row)

print("✅ Connection and query test successful!")
