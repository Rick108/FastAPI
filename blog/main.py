from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

myApp = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# store data to DB
# session is not a pydantic so use Depends(get_db)
# set HTML status code for created using FastAPI status module
@myApp.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        return e


# retrieve all blogs from DB
# we need to declare the request_model as list of
# schema.blog as we need a list of entries
@myApp.get('/blog', response_model=List[schemas.Blog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# retrieve blog by id and giving the first match only
# default status code is 200 but we can override it based on situation
# request_model is a pydantic model (schemas), which only shows the values for the schema
# the ShowBlog schema is defined in schemas
@myApp.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}

        # instead of two upper lines we can also raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
    return blog


# Delete a blog
@myApp.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    # loading the blog and deleting
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


# update a blog, we take the request to get new entry
@myApp.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.update(request.dict())  # passing the request body fully in update
    db.commit()
    return 'updated successfully!!'


# Create user, using post request
@myApp.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    try:
        new_user = models.User(name=request.name, email=request.email, password=request.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        return e
