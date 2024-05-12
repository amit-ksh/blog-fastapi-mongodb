from models.user import User
from database.database import user_collection


class UserService:
    """User service class
    """
    @classmethod
    async def add_user(cls, new_user: User) -> User:
        """Create new user

        Args:
            new_user (User): new user data

        Returns:
            User: new user data
        """
        user = await new_user.create()
        return user
