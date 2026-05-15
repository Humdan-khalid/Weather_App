from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from app.database_models.users_table import Users

class UserHistory(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    city_name: str = Field(nullable=False)
    temperature: float = Field(nullable=False)
    feels_like: float = Field(nullable=False)
    humidity: int = Field(nullable=False)
    wind: float = Field(nullable=False)
    weather: str = Field(nullable=False)
    description: str = Field(nullable=False)
    time: str = Field(nullable=False)

class ReadWeather(BaseModel):
    city_name: str
    temperature: float
    feels_like: float
    humidity: int
    wind: float
    weather: str
    description: str