from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

#This sets the schema of the table

#Manny ways to populate the azure sql instance.
#Step 1 -> Change environement variables in .env so they point to sql instance in azure
#Step 2 -> THen change this file with the tables(schema) we need - rename tables with names we want and columns and columsn types
#Step 3 => Then change init_db file. This file you have to change completely because right now is adding individual records you need more efficient method. 
#You will run this file init_db and sql instance in azure will get populated

#Then make sure the english to sql works in azure. Once this works we can move the code from local to cloud


Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
