from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends

from auth.auth import get_current_user
from schemas.blog import UpdateBlogModel, CreateBlogModel
from schemas.response import Response
from services.blog import BlogService
from models.user import User

router = APIRouter()


@router.get("/", response_description="All blogs retrieved", response_model=Response)
async def get_all_blogs():
    """Get all blogs

    Returns:
        blogs: list of blogs
    """
    blogs = await BlogService.get_all()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "All blogs data retrieved successfully",
        "data": blogs,
    }


@router.get("/{id}", response_description="Blog retrieved", response_model=Response)
async def get_blog(
    blog_id: PydanticObjectId,
):
    """Get blog by id

    Args:
        blog_id (PydanticObjectId): _description_

    Returns:
        _type_: _description_
    """
    blog = await BlogService.get(blog_id)
    if blog:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Blog data retrieved successfully",
            "data": blog,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Blog doesn't exist",
    }


@router.post(
    "/",
    response_description="Blog added into the database",
    response_model=Response,
)
async def create_blog(
    blog: CreateBlogModel = Body(...),
    current_user: User = Depends(get_current_user),
):
    """Create blog

    Args:
        blog (Blog): blog data

    Returns:
        response: Response
    """
    new_blog = await BlogService.create(blog, current_user.id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Blog created successfully",
        "data": new_blog,
    }


@router.delete("/{id}", response_description="Blog deleted from the database")
async def delete_blog(
    blog_id: PydanticObjectId, current_user: User = Depends(get_current_user)
):
    """Delte blog by id

    Args:
        blog_id (PydanticObjectId): blog id

    Returns:
        response: Response
    """
    deleted_blog = await BlogService.delete(blog_id, current_user.id)
    if deleted_blog:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Blog deleted",
            "data": deleted_blog,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Blog doesn't exist",
        "data": None,
    }


@router.patch("/{id}", response_model=Response)
async def update_blog(
    blog_id: PydanticObjectId,
    req: UpdateBlogModel = Body(...),
    current_user: User = Depends(get_current_user),
):
    """Update blog by id

    Args:
        blog_id (PydanticObjectId): blog id
        req (UpdateBlogModel, optional): updated blog data

    Returns:
        response: Response
    """
    updated_blog = await BlogService.update(blog_id, req.dict(), current_user.id)
    if updated_blog:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Blog updated",
            "data": updated_blog,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Blog not found",
        "data": None,
    }
