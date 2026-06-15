from fastapi import FastAPI , HTTPException , Depends , Query
from sqlalchemy.orm import Session
from databse import engine, SessionLocal
import models, shema
from auth import create_tokken, verify_tokken

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  



@app.post("/login")
def login():
    return{
        "access_token":create_tokken({"sub":"admin"}),
        "token_type": "bearer"
    }


@app.get("/")
def home():
    return{
        "massage":"Blog api started"
    }

@app.post("/blogs", response_model = shema.BlogResponce)
def create_blog(blog : shema.BlogCreate , db:Session= Depends(get_db), user = Depends(verify_tokken)):
    print(models.Blog.__table__.columns.keys())
    new_blog= models.Blog(
        title = blog.title,
        content = blog.content
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




@app.get("/blog")
def read_blogs(page:int=1, limit:int=5, search:str=Query(default=""),db:Session=Depends(get_db)):
    query=db.query(models.Blog)
    if search:
        query= query.filter(models.Blog.title.ilike(f"%{search}%"))
    total = query.count()
    start = (page -1)*limit
    blog = query.offset(start).limit(limit).all()  

    return{
        "page": page,
        "limit":limit,
        "total":total,
        "data":blog
    } 

@app.get("/blog/{id}", response_model= shema.BlogResponce )
def read_blog(id:int, db:Session=Depends(get_db )):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code= 404,
            detail= "id not found"
        )
    return blog


@app.put("/blog/{id}",  response_model= shema.BlogResponce)
def update_blog(id:int, blog:shema.BlogCreate,db:Session=Depends(get_db ), user=Depends(verify_tokken)):
    existing_blog= db.query(models.Blog).filter(models.Blog.id == id).first()

    if not existing_blog :
        raise HTTPException(
            status_code= 404,
            detail= "id not found"
        )
    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()

    return existing_blog

@app.delete("/blog/{id}")
def delete(id : int, db:Session=Depends(get_db ), user = Depends(verify_tokken)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code= 404,
            detail="Blog not found"
        )
    
    blog.delete()
    db.commit()

    return{
        "massage":"This blog is deleted"
    }

