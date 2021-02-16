from tronclass_cli.middleware import Middleware


class Command(Middleware):
    name = None

    def __init__(self, parser, ctx):
        super().__init__(parser, ctx)
        self._sub_parsers = None

    def add_sub_command(self, name: str, sub_command_class):
        if self._sub_parsers is None:
            self._sub_parsers = self._parser.add_subparsers()
        sub_parser = self._sub_parsers.add_parser(name)
        obj = sub_command_class(sub_parser, self._ctx)
        return obj
