#business as usual import the modules
from pydantic import BaseModel,constr,validator,EmailStr

#define how the user input will look like more like serializing
class User(BaseModel):
    name:constr(min_length=2, max_length=50)
    email: EmailStr
    password: str

#the user outpu will look like this
class DisplayUser(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
