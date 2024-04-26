import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Create an SQLite in-memory database and echo the SQL commands executed
engine = create_engine('sqlite:///data/heart.sqlite', echo=True)

# Define a base class for the table schema
Base = declarative_base()


# Define the table structure, corresponding to the CSV structure
class Heart(Base):
    __tablename__ = 'heart'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    sexe = Column(String)
    type_douleur = Column(String)
    pression = Column(Integer)
    cholester = Column(Integer)
    sucre = Column(String)
    electro = Column(String)
    taux_max = Column(Integer)
    angine = Column(String)
    depression = Column(Float)
    pic = Column(Integer)
    vaisseau = Column(String)
    coeur = Column(String)


# Create all tables in the database (this creates the 'heart' table)
Base.metadata.create_all(engine)

# Read CSV file into a DataFrame
df = pd.read_csv('data/heart.csv')

# Create a Session to handle updates
Session = sessionmaker(bind=engine)
session = Session()

# Write the records stored in the DataFrame to the SQL database
df.to_sql('heart', con=engine, index_label='id', if_exists='replace')

# Optionally, verify data insertion
for instance in session.query(Heart).order_by(Heart.id):
    print(instance.age, instance.sexe, instance.type_douleur)