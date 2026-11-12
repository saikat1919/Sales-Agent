import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.modules.users.models import Role


class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class ReadUser(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    role: Role

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

