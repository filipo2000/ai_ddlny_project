from db import engine
from models import Base, Product
from sqlalchemy.orm import Session

#THIS CREATES TABLES IN POSTGRE SQL DATABASE

# Drop all tables and recreate (optional)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Seed sample data
sample_products = [
    Product(name="Widget A", price=19.99, quantity=100),
    Product(name="Widget B", price=29.99, quantity=50),
    Product(name="Widget C", price=9.99, quantity=200),
]

with Session(engine) as session:
    session.add_all(sample_products)
    session.commit()

print("✅ Tables created and sample data inserted!")
