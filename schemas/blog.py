from typing import Optional
from pydantic import BaseModel


class UpdateBlogModel(BaseModel):
    """Update blog data model"""

    title: Optional[str]
    content: Optional[str]

    class Config:
        """Config"""

        json_schema_extra = {
            "example": {"title": "Blog title", "content": "Blog content"}
        }


class CreateBlogModel(BaseModel):
    """Update blog data model"""

    title: str
    content: str

    class Config:
        """Config"""

        json_schema_extra = {
            "example": {"title": "Blog title", "content": "Blog content"}
        }
