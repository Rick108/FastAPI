from pydantic import BaseModel


# this schema is used for post method
class Blog(BaseModel):
    title: str
    body: str


# we need to make orm true like this as we are using,
# this schema for get request, we can define what
# parameters do we need (title,body,id)
class ShowBlog(BaseModel):
    # will show only title
    title: str

    class Config:
        orm_mode = True


class User(BaseModel):
    email: str
    password: str
    name: str

