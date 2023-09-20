from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog,user, photo, authentication


myApp = FastAPI()

models.Base.metadata.create_all(engine)

myApp.include_router(blog.router)
myApp.include_router(user.router)
myApp.include_router(photo.router)
myApp.include_router(authentication.router)













