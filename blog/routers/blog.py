from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs'],
    dependencies=[Depends(oauth2.get_current_user)]
)


# retrieve all blogs from DB
# we need to declare the request_model as list of
# schema.blog as we need a list of entries
@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)





# store data to DB
# session is not a pydantic so use Depends(get_db)
# set HTML status code for created using FastAPI status module
# we can assign tags to define the method, only for documentation.
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


# retrieve blog by id and giving the first match only
# default status code is 200 but we can override it based on situation
# request_model is a pydantic model (schemas), which only returns the values for the schema
# the ShowBlog schema is defined in schemas. Response is what we get
# after doing a request, response_model defines what to return in Response.
# It is for any kind of requests(get, post...).
@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(database.get_db)):
    return blog.show(id, db)


# Delete a blog
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)


# update a blog, we take the request to get new entry
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)
