from pydantic import BaseModel, EmailStr, constr, field_validator

from app.dao.base import validation_password

PasswordType = constr(min_length=6)

class SUserSchemas(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str

    @field_validator('hashed_password')
    def validate_password(cls, v:str):
        return validation_password(v)


class SUserLoginSchemas(BaseModel):
    email: EmailStr
    password: str


class SUserSchemasUpdate(BaseModel):
    email: EmailStr
    name: str
    role: str
    balance: int

class SUserSchemasUpdatePass(BaseModel):
    email: EmailStr
    password:PasswordType

    @field_validator('password')
    def validate(cls, v: str):
        return validation_password(v)

