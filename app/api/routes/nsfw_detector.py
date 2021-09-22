from fastapi import APIRouter, HTTPException, FastAPI
from app.api.handlers.nsfw_detector import detect
from typing import Optional
from pydantic import BaseModel
from starlette.responses import JSONResponse
import io


class Image(BaseModel):
    url: str


router = APIRouter()


# post because I don't want to deal with url
@router.post("/")
def upscale_url(image: Image):
    result = detect(image.url)
    if result is None:
        raise HTTPException(status_code=400, detail="url not found")
    return JSONResponse(result)
