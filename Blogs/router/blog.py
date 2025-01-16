from typing import List
from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from . import oauth2  # Updated import
from .. import schemas , database
from ..repository import blog


router = APIRouter(
    tags=['Blogs'],
    prefix="/blogs",
)
get_db = database.get_db


@router.get('/',response_model=list[schemas.ShowBlog])
def get_all_blogs(db:Session = Depends(get_db),current_user: schemas.User=Depends(oauth2.get_current_user)):
        return blog.get_all(db)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blogs(request: schemas.Blog,db:Session = Depends(get_db),current_user: schemas.User=Depends(oauth2.get_current_user)):
    return blog.create(request,db)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,db:Session = Depends(get_db),current_user: schemas.User=Depends(oauth2.get_current_user)):
    return blog.delete(id,db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_specific_blog(id: int, db: Session = Depends(get_db),current_user: schemas.User=Depends(oauth2.get_current_user)):
    return blog.get_specific_blog(id, db)


@router.put('/{id}')
def update_blog(id:int,request:schemas.Blog,db:Session = Depends(get_db),current_user: schemas.User=Depends(oauth2.get_current_user)):
    return blog.update_blog(id,request,db)
