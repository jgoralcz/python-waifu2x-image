from fastapi import APIRouter

from app.api.routes import upscale, nsfw_detector, hashes

router = APIRouter()
router.include_router(upscale.router, tags=["upscaler"], prefix="/upscales")
router.include_router(nsfw_detector.router, tags=["detector"], prefix="/detects")
router.include_router(hashes.router, tags=["hash"], prefix="/hash")
