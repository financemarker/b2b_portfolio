import logging
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from backend.schemas.response_wrapper import ApiResponse

logger = logging.getLogger("inport")


def register_exception_handlers(app: FastAPI) -> None:
    """Подключает единые обработчики ошибок для всего API."""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"{exc.status_code} {exc.detail} @ {request.url.path}")

        response = ApiResponse.fail(exc.status_code, str(exc.detail))
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(response)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.info(f"Validation error @ {request.url.path}")

        # Извлекаем краткое сообщение (можно улучшить при желании)
        messages = [err.get("msg", "") for err in exc.errors()]
        message = "; ".join(messages) or "Validation error"

        response = ApiResponse.fail(422, message)
        return JSONResponse(status_code=422, content=jsonable_encoder(response))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception @ {request.url.path}: {exc}")

        response = ApiResponse.fail(500, "Internal server error")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(response)
        )
