from fastapi import HTTPException, status

UserAlreadyExitsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exits'
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect email or password'
)


InvalidTokenException = HTTPException(
    status_code=401,
    detail="Invalid token"
)

TokenExpiredException = HTTPException(
    status_code=401,
    detail="Token expired"
)

UserIdDoesNotExitsException = HTTPException(
    status_code=401,
    detail="User_id does not exits"
)

UserDoesNotExitsException = HTTPException(
    status_code=401,
    detail="User does not exits"
)

