from typing import List
from beanie import PydanticObjectId

from models.blog import Blog
from schemas.blog import UpdateBlogModel, CreateBlogModel
from database.database import blog_collection


class BlogService:
    """Blog service class"""

    @classmethod
    async def get_all(cls) -> List[Blog]:
        """Retrieve all blogs

        Returns:
            List[Blog]: list of blogs
        """
        blogs = await blog_collection.all().to_list()
        return blogs

    @classmethod
    async def get(cls, blog_id: PydanticObjectId) -> Blog:
        """Retrieve blog by id

        Args:
            blog_id (str): blog id

        Returns:
            Blog: blog data
        """
        blog = await blog_collection.get(blog_id)
        return blog

    @classmethod
    async def get_blogs_by_user_id(cls, user_id: PydanticObjectId) -> List[Blog]:
        """Retrieve blogs by user id

        Args:
            user_id (str): user id

        Returns:
            List[Blog]: list of blogs
        """
        blogs = await blog_collection.find_many(Blog.user_id == user_id).to_list()
        return blogs

    @classmethod
    async def create(cls, new_blog: CreateBlogModel, user_id: PydanticObjectId) -> Blog:
        """Create new blog

        Args:
            new_blog (Blog): new blog data

        Returns:
            Blog: new blog data
        """
        blog = await blog_collection.create({**new_blog.dict(), "author": user_id})
        return blog

    @classmethod
    async def delete(cls, blog_id: PydanticObjectId, user_id: PydanticObjectId) -> bool:
        """Delete blog by id

        Args:
            blog_id (str): blog id

        Returns:
            bool: True if blog is deleted
        """
        blog = await blog_collection.find_one(
            Blog.id == blog_id, Blog.author == user_id
        )
        if blog:
            await blog.delete()
            return True
        return False

    @classmethod
    async def update(
        cls, blog_id: PydanticObjectId, data: UpdateBlogModel, user_id: PydanticObjectId
    ) -> Blog:
        """Update blog data

        Args:
            blog_id (str): blog id
            data (dict): blog data

        Returns:
            Blog: updated blog data
        """
        blog = await blog_collection.blog.find_one(
            Blog.id == blog_id, Blog.author == user_id
        )
        if not blog:
            return None
        blog.title = data.title or blog.title
        blog.content = data.content or blog.content
        return blog
