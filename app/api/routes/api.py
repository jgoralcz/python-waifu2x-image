from fastapi import APIRouter

from app.api.routes import upscale, nsfw_detector

router = APIRouter()
router.include_router(upscale.router, tags=["upscaler"], prefix="/upscales")
router.include_router(nsfw_detector.router, tags=["detector"], prefix="/detects")
