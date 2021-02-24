from tronclass_cli.api import Api
from tronclass_cli.middleware import Middleware
from tronclass_cli.middleware.session import SessionMiddleware

api_urls = {
    'zju': 'https://courses.zju.edu.cn'
}


class ApiMiddleware(Middleware):
    name = 'api'
    middleware_classes = [SessionMiddleware]

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--api-url',
                           help=f'base url of TronClass API, supported shortcuts: {", ".join(api_urls.keys())}')

    def _exec(self, args):
        api_url = api_urls.get(args.api_url, args.api_url)
        self._ctx.api = Api(api_url, self._ctx.username, self._ctx.cache, self._ctx.session)
