from pydantic import BaseModel, EmailStr, constr, Field

PasswordType = constr(min_length=6)

class SUserSchemas(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str

class SUserLoginSchemas(BaseModel):
    email: EmailStr
    password: PasswordType

class SUserSchemasUpdate(BaseModel):
    email: EmailStr
    name: str
    role: str

class SUserSchemasUpdatePass(BaseModel):
    email: EmailStr
    password:PasswordType
