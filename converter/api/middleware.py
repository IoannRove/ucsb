import logging
from http import HTTPStatus
from typing import Mapping, Optional

from aiohttp import JsonPayload, web
from aiohttp.web_exceptions import (
    HTTPBadRequest, HTTPException, HTTPInternalServerError,
)
from aiohttp.web_request import Request
from marshmallow import ValidationError

log = logging.getLogger(__name__)


def format_http_error(http_error_cls, message: Optional[str] = None,
                      fields: Optional[Mapping] = None) -> HTTPException:
    """
    Форматирует ошибку в виде HTTP исключения
    """
    status = HTTPStatus(http_error_cls.status_code)
    error = {
        'code': status.name.lower(),
        'message': message or status.description
    }

    if fields:
        error['fields'] = fields

    return http_error_cls(body={'error': error})


def handle_validation_error(error: ValidationError, *_):
    """
    Представляет ошибку валидации данных в виде HTTP ответа.
    """
    raise format_http_error(HTTPBadRequest, 'Request validation has failed',
                            error.messages)


@web.middleware
async def error_middleware(request: Request, handler):
    try:
        return await handler(request)
    except HTTPException as err:
        if not isinstance(err.body, JsonPayload):
            err = format_http_error(err.__class__, err.text)
        return err
    except ValidationError as err:
        return handle_validation_error(err)
    except Exception as err:
        log.exception(err)
        return format_http_error(HTTPInternalServerError)
