from typing import List, Union
from beanie import PydanticObjectId

from models.comment import Comment
from database.database import comment_collection


class CommentService:
    """Comment service class"""

    @classmethod
    async def get_all(cls) -> List[Comment]:
        """Retrieve all comments

        Returns:
            List[Comment]: list of comments
        """
        comments = await comment_collection.all().to_list()
        return comments

    @classmethod
    async def get(cls, comment_id: PydanticObjectId) -> Comment:
        """Retrieve comment by id

        Args:
            comment_id (str): comment id

        Returns:
            Comment: comment data
        """
        comment = await comment_collection.get(comment_id)
        return comment

    @classmethod
    async def get_comments_by_blog_id(cls, blog_id: PydanticObjectId) -> List[Comment]:
        """Retrieve comments by blog id

        Args:
            blog_id (str): blog id

        Returns:
            List[Comment]: list of comments
        """
        comments = await comment_collection.find_many(
            Comment.blog_id == blog_id
        ).to_list()
        return comments

    @classmethod
    async def create(
        cls, content: str, blog_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> Union[Comment, None]:
        """Create new comment

        Args:
            new_comment (comment): new comment data

        Returns:
            comment: new comment data
        """
        comment = await comment_collection.create(
            {"content": content, "blog_id": blog_id, "user_id": user_id}
        )
        if not comment:
            return None
        comment.blog_id.comments.append(comment.id)
        return comment

    @classmethod
    async def delete(
        cls, blog_id: PydanticObjectId, user_id: PydanticObjectId
    ) -> Union[Comment, None]:
        """Delete comment by id

        Args:
            comment_id (str): comment id
        """
        comment = await comment_collection.delete(blog_id, user_id)
        if not comment:
            return None
        return comment
