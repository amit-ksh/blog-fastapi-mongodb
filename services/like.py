from typing import List, Union
from beanie import PydanticObjectId

from models.like import Like
from database.database import like_collection


class LikeService:
    """Like service class"""

    @classmethod
    async def get_all(cls) -> List[Like]:
        """Retrieve all likes

        Returns:
            List[Like]: list of likes
        """
        likes = await like_collection.all().to_list()
        return likes

    @classmethod
    async def get(cls, like_id: PydanticObjectId) -> Like:
        """Retrieve like by id

        Args:
            like_id (str): like id

        Returns:
            Like: like data
        """
        like = await like_collection.get(like_id)
        return like

    @classmethod
    async def get_likes_by_blog_id(cls, blog_id: PydanticObjectId) -> List[Like]:
        """Retrieve likes by blog id

        Args:
            blog_id (str): blog id

        Returns:
            List[Like]: list of likes
        """
        likes = await like_collection.find_many(Like.blog_id == blog_id).to_list()
        return likes

    @classmethod
    async def create(
        cls, blog_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> Union[Like, None]:
        """Create new like

        Args:
            new_like (Like): new like data

        Returns:
            Like: new like data
        """
        like = await like_collection.create({"blog_id": blog_id, "user_id": user_id})
        if not like:
            return None
        like.blog_id.likes.append(like.id)
        return like

    @classmethod
    async def delete(
        cls, blog_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> Union[Like, None]:
        """Delete like by id

        Args:
            like_id (str): like id
        """
        like = await like_collection.delete(blog_id, user_id)
        if not like:
            return None
        return like
