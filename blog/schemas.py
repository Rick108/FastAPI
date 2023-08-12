from pydantic import BaseModel
from typing import List


# this schema is used for post method
class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        from_attributes = True


class User(BaseModel):
    email: str
    password: str
    name: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        from_attributes = True


# we need to make orm true like this as we are using,
# this schema for get request, we can define what
# parameters do we need (title,body,id)
class ShowBlog(BaseModel):
    # will show only title
    title: str
    body: str
    creator: ShowUser

    class Config:
        from_attributes = True
# as creator is SHowUser type we need to keep the
# creator after ShowUser func


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
