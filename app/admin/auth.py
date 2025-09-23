from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime

from app.users.auth import auth_user, create_access_token
from app.users.dao import UserDAO
from app.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await auth_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            return False

        expire = payload.get("exp")
        if not expire or (int(expire) < datetime.utcnow().timestamp()):
            return False

        user_id = payload.get("sub")
        if not user_id:
            return False

        user = await UserDAO.find_one_ore_none(id=int(user_id))
        if not user:
            return False

        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для входа в админку",
            )

        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
