from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

myApp = FastAPI()


# in dynamic routing take care of the order
# of matching, here blog/int will not match
# with bolg/unpublished, so it will rerouted
# to blog/{id}, {} means anything.
@myApp.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the database '}
    else:
        return {'data': f'{limit} blogs from the database'}


@myApp.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@myApp.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@myApp.get('/blog/{id}/comments')
# first is path parameter, second one is path parameter
def comments(id, limit=10):
    return {'data': {'1', '2'}}



# for posting we need to create pydantic model
# and pass the model as a parameter to post.

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@myApp.post('/blog')
def create_blog(blog: Blog):
    import pdb; pdb.set_trace();
    print(blog)
    return f'Blog id created with title: {blog.title}'


# Pydantic schemas
#  CRUD operations
# It is done in the blog env

