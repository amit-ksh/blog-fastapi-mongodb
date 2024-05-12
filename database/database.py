from typing import List, Union
from beanie import PydanticObjectId

from models.user import User
from models.blog import Blog
from models.like import Like
from models.comment import Comment

user_collection = User
blog_collection = Blog
like_collection = Like
comment_collection = Comment


async def retrieve_blogs() -> List[Blog]:
    blogs = await blog_collection.all().to_list()
    return blogs


async def add_blog(new_blog: Blog) -> Blog:
    blog = await new_blog.create()
    return blog


async def retrieve_blog(id: PydanticObjectId) -> Blog:
    blog = await blog_collection.get(id)
    if blog:
        return blog


async def delete_blog(id: PydanticObjectId) -> bool:
    blog = await blog_collection.get(id)
    if blog:
        await blog.delete()
        return True


async def update_blog_data(id: PydanticObjectId, data: dict) -> Union[bool, Blog]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {
        "$set": {field: value for field, value in des_body.items()}}
    blog = await blog_collection.get(id)
    if Blog:
        await blog.update(update_query)
        return blog
    return False
