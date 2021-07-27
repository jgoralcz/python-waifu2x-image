from fastapi import APIRouter, HTTPException, FastAPI
from app.api.handlers.upscale import upscale
from typing import Optional
from pydantic import BaseModel
from starlette.responses import StreamingResponse
import io


class Image(BaseModel):
    url: str


router = APIRouter()


# post because I don't want to deal with url
@router.post("/")
def upscale_url(image: Image):
    upscaled = upscale(image.url)
    if upscaled is None:
        raise HTTPException(status_code=400, detail="url not found")
    return StreamingResponse(io.BytesIO(upscaled))
