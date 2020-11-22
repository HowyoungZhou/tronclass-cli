from tronclass_cli.command import Command
from tronclass_cli.middleware.session import SessionMiddleware


class TodoCommand(Command):
    name = 'todo'
    middleware_classes = [SessionMiddleware]

    def _init_parser(self):
        pass

    def _exec(self, args):
        pass
