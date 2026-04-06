from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel, constr, validator
from datetime import datetime


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=30, nullable=False)
    age: int = Field(ge=18, le=100, nullable=False)
    phone_number: str = Field(min_length=11, max_length=11, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(min_length=8, max_length=25, nullable=False)
    created_at: datetime = datetime.now()

class CreateUsers(BaseModel):
    name: str = Field(min_length=3, max_length=35, regex=r"^[a-zA-Z]+$")
    age: int = Field(ge= 18, le=99)
    phone_number: str = Field(regex=r"^03[0-9]{9}$")
    email: EmailStr 
    password: str = Field(min_length=8, max_length=25)

    @validator("name")
    def validate_name(cls, name):
        import re
        if not re.fullmatch("^[a-zA-Z ]{3,35}$", name):
            raise ValueError("name must be letters.")
        return name

    @validator("phone_number")
    def validate_phone_number(cls, number):
        import re
        if not re.fullmatch("^03[0-9]{9}$", number):
            raise ValueError("phone number must start to 03 and 11 numbers should have.")
        return number
    
    @validator("email")
    def validate_email(cls, user_email):
        import re
        if not re.fullmatch("^[a-z][a-z0-9]+@gmail\.com$", user_email):
            raise ValueError("please type the proper email.")
        return user_email

class ReadUser(BaseModel):
    id: int
    name: str
    age: int
    phone_number: str
    email: EmailStr

class UsersLogin(BaseModel):
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    access_token: str
    token_type: str

class UserHistory(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str = Field(min_length=3, max_length=30, nullable=False)
    city_name: str = Field(nullable=False)
    temperature: str = Field(nullable=False)
    feels_like: str = Field(nullable=False)
    humidity: str = Field(nullable=False)
    wind: str = Field(nullable=False)
    weather: str = Field(nullable=False)
    description: str = Field(nullable=False)
    time: str = Field(nullable=False)


class Admins(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=35, nullable=False)
    age: float = Field(ge=17, le=100, nullable=False)
    phone_number: str = Field(min_length=11, max_length=11, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length=12, max_length=30)
    created_at: datetime = datetime.now()


class CreateAdmin(BaseModel):
    name: str = Field(min_length=3, max_length=35, nullable=False)
    age: float = Field(ge=17, le=100, nullable=False)
    phone_number: str = Field(min_length=11, max_length=11, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length=12, max_length=30)

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
            raise ValueError("Invalid number style")
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
