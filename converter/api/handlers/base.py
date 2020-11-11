from aiohttp.web_urldispatcher import View


class BaseView(View):
    URL_PATH: str

    @property
    def redis(self):
        return self.request.app['redis']
