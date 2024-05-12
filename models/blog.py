from datetime import datetime
from typing import Optional, List


from beanie import Document, Link

from .user import User
from .like import Like
from .comment import Comment


class Blog(Document):
    """Blog model"""

    title: str
    content: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    author: Link[User]

    likes: List[Link[Like]] = []
    comments: List[Link[Comment]] = []

    class Settings:
        name = "blog"
