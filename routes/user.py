from fastapi import Body, APIRouter, HTTPException

from services.user import UserService
from models.user import User, UserData, UserSignIn
from auth.auth import hash_helper, create_access_token

router = APIRouter()


@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    """Check user credentials and return access token if valid

    Args:
        user_credentials (UserSignIn, optional): User credentials. Defaults to Body(...).

    Raises:
        HTTPException: Raise exception if user credentials are invalid

    Returns:
        str: JWT token
    """
    user_exists = await User.find_one(User.email == user_credentials.username)
    if user_exists:
        valid = hash_helper.verify(user_credentials.password, user_exists.password)
        if valid:
            return create_access_token(
                {"id": user_exists.id, "email": user_exists.email}
            )

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")


@router.post("/signup", response_model=UserData)
async def user_signup(user: User = Body(...)):
    """Create new user

    Args:
        user (User, optional): user data. Defaults to Body(...).

    Raises:
        HTTPException: Raise exception if user with email already exists

    Returns:
        User: new user data
    """
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    new_user = await UserService.add_user(user)
    return new_user
