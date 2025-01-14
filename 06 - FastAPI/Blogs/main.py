from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas , models 
from .database import engine , SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Now get blogs from database 
@app.get('/blogs',response_model=list[schemas.ShowBlog],tags=['Blogs'])
def get_all_blogs(db:Session = Depends(get_db)):
        blogs = db.query(models.Blog).all()
        return blogs


@app.post('/blogs',status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create_blogs(request: schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'Blogs':f'Blog is created with a name of {new_blog.title}'}


@app.delete('/blogs/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def delete_blog(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Blogs':f'Blog is deleted with a name of {id}'}

@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,tags=['Blogs'])
def get_specific_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blogs


@app.put('/blogs/{id}',tags=['Blogs'])
def update_blog(id:int,request:schemas.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
    else:
        blog.title = request.title
        blog.body = request.body
        db.commit()
        return {'blog':f'Blog is updated with a name of {blog.title}'}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/users',response_model=schemas.ShowUser,tags=['Users'])
def create_user(request:schemas.User,db:Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name,email=request.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['Users'])
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user