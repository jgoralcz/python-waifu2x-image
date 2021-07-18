import secrets
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.exceptions import HTTPException
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from environs import Env

env = Env()
env.read_env()
security = HTTPBasic()


async def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, env("USERNAME"))
    correct_password = secrets.compare_digest(credentials.password, env("PASSWORD"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_application():
    application = FastAPI(
        title="Image API",
        debug=False,
        version="1.0.0",
        dependencies=[Depends(basic_auth)],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix="/api")

    return application


app = get_application()
