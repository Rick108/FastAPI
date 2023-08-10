from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from . hashing import Hash

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
# we can assign tags to define the method, only for documentation.
@myApp.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        return e


# retrieve all blogs from DB
# we need to declare the request_model as list of
# schema.blog as we need a list of entries
@myApp.get('/blog', response_model=List[schemas.Blog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# retrieve blog by id and giving the first match only
# default status code is 200 but we can override it based on situation
# request_model is a pydantic model (schemas), which only returns the values for the schema
# the ShowBlog schema is defined in schemas. Response is what we get
# after doing a request, response_model defines what to return in Response.
# It is for any kind of requests(get, post...).
@myApp.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}

        # instead of two upper lines we can also raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
    return blog


# Delete a blog
@myApp.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
    # loading the blog and deleting
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


# update a blog, we take the request to get new entry
@myApp.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.update(request.dict())  # passing the request body fully in update
    db.commit()
    return 'updated successfully!!'


# Create user, using post request
@myApp.post('/user', response_model= schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    try:
        # encrypting the password using hashing.py file
        new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        return e


# get user
@myApp.get('/user/{id}', response_model= schemas.ShowUser, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


# Relationship should be created as every blog should
# belong to an owner(user), so we need to establish a relationship
# b/w blogs and users. It is implemented in models file.
