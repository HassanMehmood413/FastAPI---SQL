from typing import List
from fastapi import FastAPI, Depends, HTTPException , status
from sqlalchemy.orm import Session
from .. import models
from .. import database

get_db = database.get_db




def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request,db:Session):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id,db:Session):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Blogs':f'Blog is deleted with a name of {id}'}

def get_specific_blog(id,db:Session):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blogs

def update_blog(id,request,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
    else:
        blog.title = request.title
        blog.body = request.body
        db.commit()
        return {'blog':f'Blog is updated with a name of {blog.title}'}