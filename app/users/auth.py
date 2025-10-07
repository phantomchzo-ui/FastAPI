from datetime import timedelta, datetime, timezone
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import UserDoesNotExitsException
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# async def auth_user(email: EmailStr, password: str):

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def auth_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_ore_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def auth_user_without_pass(email: EmailStr):
    user = await UserDAO.find_one_ore_none(email=email)
    if not user:
        raise UserDoesNotExitsException
    return user

