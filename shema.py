from pydantic import BaseModel

class BlogCreate(BaseModel):
    title:str
    content:str

class BlogResponce(BaseModel):
    id: int
    title:str
    content:str

    class Config:
        from_attributes = True