from beanie import Document, PydanticObjectId


class Like(Document):
    """Like model"""

    user: PydanticObjectId
    blog: PydanticObjectId

    class Settings:
        name = "like"
