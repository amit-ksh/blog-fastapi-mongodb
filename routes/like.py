from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from auth.auth import get_current_user
from schemas.response import Response
from services.like import LikeService

router = APIRouter()


@router.get(
    "/blog/{blog_id}",
    response_description="All likes retrieved",
    response_model=Response,
)
async def get_all_likes(blog_id: PydanticObjectId):
    """Get all likes by blog id

    Args:
        blog_id (PydanticObjectId): blog id

    Returns:
        likes: list of likes
    """
    likes = await LikeService.get_likes_by_blog_id(blog_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "All likes data retrieved successfully",
        "data": likes,
    }


@router.post(
    "/blog/{blog_id}",
    response_description="Like added into the database",
    response_model=Response,
)
async def create_like(
    blog_id: PydanticObjectId, current_user: dict = Depends(get_current_user)
):
    """Create like

    Args:
        blog_id (str): Blog ID

    Returns:
        like: new like data
    """
    new_like = await LikeService.create(blog_id, current_user.id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Like added successfully",
        "data": new_like,
    }


@router.delete(
    "/{like_id}",
    response_description="Like deleted from the database",
    response_model=Response,
)
async def delete_like(
    blog_id: PydanticObjectId, current_user: dict = Depends(get_current_user)
):
    """Delete like

    Args:
        blog_id (PydanticObjectId): blog id

    Returns:
        Like: like data
    """
    response = await LikeService.delete(blog_id, current_user.id)
    if response:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Like deleted successfully",
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Like doesn't exist",
    }
