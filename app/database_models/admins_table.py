from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel, constr, validator
from datetime import datetime

class Admins(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=35, nullable=False)
    age: float = Field(ge=17, le=100, nullable=False)
    phone_number: str = Field(min_length=11, max_length=11, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length=12, max_length=100)
    created_at: datetime = datetime.now()


class CreateAdmin(BaseModel):
    name: str = Field(min_length=3, max_length=35, nullable=False)
    age: float = Field(ge=17, le=100, nullable=False)
    phone_number: str = Field(min_length=11, max_length=11, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length=12, max_length=100)

    @validator("name")
    def validate_name(cls, name: str):
        import re
        if not re.fullmatch("^[a-zA-Z ]{3,35}$", name):
            raise ValueError("name must be letters")
        return name
    
    @validator("phone_number")
    def validate_phone_number(cls, phone_number: str):
        import re
        if not re.fullmatch("^03[0-9]{9}$", phone_number):
            raise ValueError("Invalid phone number")
        else:
            return phone_number
        
    @validator("email")
    def validate_email(cls, email: EmailStr):
        import re
        if not re.fullmatch("^[a-z][a-z0-9]+@gmail\.com$", email):
            raise ValueError("Invalid email style")
        return email

class ReadAdmin(BaseModel):
    id: int
    name: str
    age: float
    phone_number: str
    email: EmailStr

class LoginAdmin(BaseModel):
    email: EmailStr
    password: str