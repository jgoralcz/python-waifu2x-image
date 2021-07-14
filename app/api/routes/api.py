from fastapi import APIRouter

from app.api.routes import upscale

router = APIRouter()
router.include_router(upscale.router, tags=["upscaler"], prefix="/upscales")
