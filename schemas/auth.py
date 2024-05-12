from typing import Union
from pydantic import BaseModel


class TokenData:
    id: Union[str, None] = None
    email: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
