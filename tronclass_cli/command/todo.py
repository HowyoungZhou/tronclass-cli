from argparse import ArgumentParser

from tronclass_cli.command import Command


class TodoCommand(Command):
    def __init__(self, parser: ArgumentParser):
        super(TodoCommand, self).__init__(parser)

    def init_parser(self):
        super(TodoCommand, self).init_parser()
