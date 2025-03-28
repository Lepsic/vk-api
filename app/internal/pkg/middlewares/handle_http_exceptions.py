

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.pkg.logger import get_logger
from app.pkg.models.base import BaseAPIException

__all__ = [
    "handle_api_exceptions",
]

logger = get_logger(__name__)


def handle_api_exceptions(exc: BaseAPIException):

    logger.info(exc)

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


