from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import *
from app.users.dao import UserDAO
from app.users.models import User


def get_token(request: Request):
    token = request.cookies.get('shop_access_token')
    if not token:
        raise HTTPException(status_code=401)
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise InvalidTokenException

    expire = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIdDoesNotExitsException
    user = await UserDAO.find_one_ore_none(id=int(user_id))
    if not user:
        raise UserDoesNotExitsException
    return user


def require_role(*roles: str):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )
        return user
    return wrapper