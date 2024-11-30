from fastapi import APIRouter

from app.api.routes import images, items, login, texts, users, utils, videos, comment_classifier

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(texts.router, prefix="/texts", tags=["texts"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(comment_classifier.router, prefix="/comment", tags=["comment classifier"])