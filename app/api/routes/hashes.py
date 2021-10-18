from fastapi import APIRouter, HTTPException, FastAPI
from app.api.handlers.imagehash import imagehashed
from typing import Optional
from pydantic import BaseModel
from starlette.responses import JSONResponse


class Image(BaseModel):
    url: str


router = APIRouter()


# post because I don't want to deal with url
@router.post("/")
def hashes(image: Image):
    result = imagehashed(image.url)
    if result is None:
        raise HTTPException(status_code=400, detail="url not found")
    return JSONResponse(result)
