from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import  create_engine

DATABASE_URL = "mysql+pymysql://root:tyson432@localhost:3306/mydatabase"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()