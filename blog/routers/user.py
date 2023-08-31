from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import database, schemas, models
from sqlalchemy.orm import Session
from repository import user



router = APIRouter(
    prefix='/user',
    tags=['users']
)




# Create user, using post request
@router.post('/', response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)




# get user
@router.get('/{id}', response_model= schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.show(id, db)


# Relationship should be created as every blog should
# belong to an owner(user), so we need to establish a relationship
# b/w blogs and users. It is implemented in models file.
