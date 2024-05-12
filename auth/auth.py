from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBasic
from passlib.context import CryptContext

from config.config import Settings
from database.database import user_collection
from schemas.auth import TokenData

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

settings = Settings()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Create access token for user

    Args:
        data (dict): data to store in token
        expires_delta (Union[timedelta, None], optional): Expiration delta. Defaults to None.

    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get current user from JWT token

    Args:
        token (Annotated[str, Depends): JWT token

    Raises:
        credentials_exception: Raise exception if credentials are invalid

    Returns:
        User: User object
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        token: str = payload.get("sub")
        if token is None:
            raise credentials_exception
        token_data = TokenData(*token)
    except jwt.PyJWTError:
        raise credentials_exception

    user = user_collection.find_one({"id": token_data.id})
    if user is None:
        raise credentials_exception
    return user
