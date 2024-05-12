from fastapi import FastAPI

from config.config import initiate_database
from routes.user import router as UserRouter
from routes.blog import router as BlogRouter
from routes.like import router as LikeRouter
from routes.comment import router as CommentRouter


app = FastAPI()


@app.on_event("startup")
async def start_database():
    """Initiate on startup"""
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    """Root route"""
    return {"message": "Hello from server"}


app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(
    BlogRouter,
    tags=["Blog"],
    prefix="/blog",
)
app.include_router(
    LikeRouter,
    tags=["Like"],
    prefix="/like",
)
app.include_router(
    CommentRouter,
    tags=["Comment"],
    prefix="/comment",
)
