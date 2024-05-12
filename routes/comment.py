from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Body

from auth.auth import get_current_user
from schemas.response import Response
from models.comment import Comment
from services.comment import CommentService

router = APIRouter()


@router.get(
    "/blog/{blog_id}",
    response_description="All comments retrieved",
    response_model=Response,
)
async def get_all_comments(blog_id: PydanticObjectId):
    """Get all comments by blog id

    Args:
        blog_id (PydanticObjectId): blog id

    Returns:
        comments: list of comments
    """
    comments = await CommentService.get_comments_by_blog_id(blog_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "All comments data retrieved successfully",
        "data": comments,
    }


@router.post(
    "/blog/{blog_id}",
    response_description="Compment added into the database",
    response_model=Response,
)
async def create_comment(
    blog_id: PydanticObjectId,
    comment: Comment = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """Create comment

    Args:
        comment (Comment): comment data

    Returns:
        comment: new comment data
    """
    new_comment = await CommentService.create(comment, blog_id, current_user.id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Comment added successfully",
        "data": new_comment,
    }


@router.delete(
    "/{comment_id}",
    response_description="Comment deleted from the database",
    response_model=Response,
)
async def delete_comment(
    comment_id: PydanticObjectId,
    current_user: dict = Depends(get_current_user),
):
    """Delete comment

    Args:
        comment_id (PydanticObjectId): comment id

    Returns:
        response: deletion status
    """
    response = await CommentService.delete(comment_id, current_user.id)
    if response:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Comment deleted successfully",
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Comment doesn't exist",
    }
