from beanie import Document, PydanticObjectId


class Comment(Document):
    """Comment model"""

    content: str
    user: PydanticObjectId
    blog: PydanticObjectId

    class Settings:
        name = "comment"
