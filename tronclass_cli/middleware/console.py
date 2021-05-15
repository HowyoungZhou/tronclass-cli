from rich.console import Console

from tronclass_cli.middleware import Middleware


class ConsoleMiddleware(Middleware):
    name = 'console'

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)

    def _exec(self, args):
        self._ctx.console = Console()

    def _dispose(self):
        pass
