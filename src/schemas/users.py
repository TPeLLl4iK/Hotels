from pydantic import BaseModel, ConfigDict


class UsersRequestAdd(BaseModel):
    #email: EmailStrL
    login: str
    password: str

class UsersAdd(BaseModel):
    #email: EmailStrL
    login: str
    hashed_password: str

class Users(BaseModel):
    #email: EmailStrL
    id: int
    login: str

    model_config = ConfigDict(from_attributes=True)

class UsersWithHashedPass(Users):
    #email: EmailStrL
    login: str
    hashed_password: str