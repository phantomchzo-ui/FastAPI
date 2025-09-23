from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExitsException, UserDoesNotExitsException
from app.users.auth import get_password_hash, auth_user, create_access_token, auth_user_without_pass, verify_password
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user, require_role
from app.users.models import User
from app.users.schemas import SUserSchemas, SUserLoginSchemas, SUserSchemasUpdate, SUserSchemasUpdatePass

router = APIRouter(prefix='/users',
    tags=['Users'])

@router.get('')
async def get_users(user: User = Depends(require_role("admin"))):
    return await UserDAO.find_all()

@router.post('/register')
async def register(user_data: SUserSchemas):
    existing_user = await UserDAO.find_one_ore_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExitsException

    hashed_password = get_password_hash(user_data.hashed_password)
    await UserDAO.add(email=user_data.email,name=user_data.name, hashed_password=hashed_password)
    return {f'{user_data.name} Вы успешно зарегались ваш эмайл! {user_data.email}'}

@router.post('/login')
async def login(user_data: SUserLoginSchemas, response: Response):
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise UserDoesNotExitsException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("shop_access_token", access_token, httponly=True)
    return access_token

@router.get('/current_user')
async def current_user(user: User = Depends(get_current_user)):
    return user

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('shop_access_token')


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, user: User = Depends(require_role("admin"))):
    return await UserDAO.remove(user_id)


@router.put('/update/{user_id}')
async def update_user(user_id: int, user_data: SUserSchemasUpdate,
                      user: User = Depends(require_role("admin"))):
    await UserDAO.update(user_id, user_data.dict())
    return {"Status": True}

@router.patch('/change_password')
async def user_forget_pass(user_data: SUserSchemasUpdatePass):
    user = await auth_user_without_pass(user_data.email)
    new_password = get_password_hash(user_data.password)

    await UserDAO.patch(user_data.email, new_password)
    return {"Status" : True}

@router.get('/verify_pass')
async def ver_pass():
    return verify_password('string12', '$2b$12$9YQrbbHwsR6GMXABKOUuoOFtiGMo8f7QEe2p7ROvRwd0BHrYbmQp.')







