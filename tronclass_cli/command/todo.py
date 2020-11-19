from argparse import ArgumentParser

from tronclass_cli.command import Command
from tronclass_cli.middleware.session import SessionMiddleware


class TodoCommand(Command):
    middlewares = [SessionMiddleware]

    def __init__(self, parser: ArgumentParser, middlewares):
        super(TodoCommand, self).__init__(parser, middlewares)

    def init_parser(self):
        super(TodoCommand, self).init_parser()

    def exec(self, args):
        super(TodoCommand, self).exec(args)
