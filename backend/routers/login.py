from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import timedelta

from core.config import settings
from core.schemas import TokenData, Token, Role
from crud.users import get_user
from crud.errors import NoSuchUserError
from crud.security import authenticate_user, create_access_token
from db.models import User
from db.session import get_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        # "me": "Access information about the current user.",
        "admin": "Admin privilege; modify shop items",
    },
)


SCOPES: dict[str, list[str]] = {"user": ["me"], "admin": ["admin", "me"]}


router = APIRouter()


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception
    try:
        user = get_user(token_data.username, db)
    except NoSuchUserError:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=401,
                detail=f"Not enough permissions, {scope} needed",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=401, detail="Deactivated user")


async def get_current_active_admin(current_user: User = Security(get_current_user)):
    if current_user.role == Role.ADMIN:
        return current_user
    raise HTTPException(status_code=401, detail="Current user is not admin")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    scopes = SCOPES.get(user.role, [])
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
