from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response
from aiohttp_apispec import docs, response_schema, querystring_schema

from converter.api.handlers.base import BaseView
from converter.api.schema import ConvertResponseSchema, ConvertRequestSchema


class ConvertView(BaseView):
    URL_PATH = '/convert'

    @docs(summary='Конвертировать валюту')
    @querystring_schema(ConvertRequestSchema)
    @response_schema(ConvertResponseSchema)
    async def get(self):
        data = self.request.rel_url.query
        val_from, val_to = await self.redis.hmget('currencies',
                                                  data.get('from'),
                                                  data.get('to'))
        if not val_from:
            raise HTTPNotFound(
                text=f'В базе нет значения для валюты {data.get("from")}')
        elif not val_to:
            raise HTTPNotFound(
                text=f'В базе нет значения для валюты {data.get("to")}')
        return Response(body={'data': {
            'amount': round(float(val_from) / float(val_to) * float(
                data.get('amount')), 2)}})
