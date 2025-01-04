from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)

from api_v1.auth.helpers import create_access_token, create_refresh_token
from auth import utils as auth_utils
from users.schemas import UserSchema
from jwt.exceptions import InvalidTokenError

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/jwt/login",
)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@dd.ru",
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not (
        auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
        )
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


async def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/users/me")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
