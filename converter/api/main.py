import logging
from typing import Mapping

from aiohttp import PAYLOAD_REGISTRY, JsonPayload
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_apispec import validation_middleware

from converter.api.handlers import HANDLERS
from converter.api.middleware import error_middleware, handle_validation_error
from converter.db.main import setup_redis


def create_app() -> Application:
    app = Application(middlewares=[error_middleware, validation_middleware])

    # Подключение на старте к redis и отключение при остановке
    app.cleanup_ctx.append(setup_redis)
    # Регистрация обработчиков
    for handler in HANDLERS:
        logging.debug('Registering handler %r as %r', handler,
                      handler.URL_PATH)
        app.router.add_route('*', handler.URL_PATH, handler)

    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping,))
    setup_aiohttp_apispec(app=app, title='Convert API', swagger_path='/docs',
                          error_callback=handle_validation_error)
    return app


def main():
    app = create_app()
    run_app(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
