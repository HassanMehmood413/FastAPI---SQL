from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.get("/")
def firstroot():
    return {'Hassan':'Mehmood'}

@app.get('/blogs')
def get_post(limit = 10,published : bool = True, sort:Optional[str] = None):

    if published:
        return {'blogs':f'{limit} published blogs from the DataBase'}
    else:
        return {'blogs':f'{limit} blogs from the DataBase'}


@app.get('/blogs/unpublished_blogs')
def unpublished_blogs():
    return {'unpublished_blogs':'All unpublished blog'}

@app.get('/blogs/{id}')
def get_blog(id: int): # Id should be ints
    return {'blog':id} 

@app.get('/blogs/{id}/comments')
def comments(id,limit=10):
    return {'id': {'1','2'}} 


# POST Section 

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]

@app.post('/blogs')
def create_blogs(request:Blog):
    return {'Blogs':f'Blog is created with a name of {request.title}'}


# if __name__== "__main__":
#     uvicorn.run(app,host='127.0.0.1',port=9000)