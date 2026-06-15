from sqlalchemy import Column,INTEGER,String,Text
from databse import Base

class Blog(Base):
    __tablename__="blog"
    id = Column(INTEGER, primary_key=True, index= True)
    title = Column(String(255))
    content = Column(Text)