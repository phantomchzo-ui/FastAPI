import re

from pydantic import BaseModel, EmailStr, constr, field_validator

PasswordType = constr(min_length=6)

class SUserSchemas(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str

    @field_validator('hashed_password')
    def validate_password(cls, v: str):
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return v


class SUserLoginSchemas(BaseModel):
    email: EmailStr
    password: str



class SUserSchemasUpdate(BaseModel):
    email: EmailStr
    name: str
    role: str

class SUserSchemasUpdatePass(BaseModel):
    email: EmailStr
    password:PasswordType
