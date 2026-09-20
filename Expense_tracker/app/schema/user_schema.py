from pydantic import BaseModel,Field,EmailStr
from datetime import datetime

class User(BaseModel):
    username: str =Field(...,min_length=3,max_length=20,description="username")
    password: str =Field(...,min_length=3,max_length=20,description="password")
    email: EmailStr =Field(...,min_length=3,max_length=20,description="email")


class UserResponse(BaseModel):
     id:int=Field(...,description="User ID")
     username:str=Field(...,description="Username")
     email:EmailStr=Field(...,description="Email")
     created_at:datetime=Field(...,description="Date and Time of User creation")
     model_config = {
         "from_attributes": True
     }

