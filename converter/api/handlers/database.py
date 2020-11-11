from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs, request_schema, querystring_schema

from converter.api.handlers.base import BaseView
from converter.api.schema import DatabaseRequestSchema, \
    DatabaseRequestQuerySchema
from converter.utils.update_curencies import update_currencies


class DatabaseView(BaseView):
    URL_PATH = '/database'

    @docs(summary='Установить данные по валютам')
    @request_schema(DatabaseRequestSchema)
    @querystring_schema(DatabaseRequestQuerySchema)
    async def post(self):
        currencies = self.request['data']['currencies']
        merge = int(self.request.rel_url.query['merge'])
        await update_currencies(self.redis, merge, currencies)
        return web.Response(status=HTTPStatus.CREATED)
