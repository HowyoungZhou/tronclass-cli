from argparse import ArgumentParser


class Command:
    middlewares = []

    def __init__(self, parser: ArgumentParser, middlewares):
        self.parser = parser
        self.middlewares = middlewares
        self.ctx = {}
        self.sub_parsers = None
        self.init_parser()

    def init_parser(self):
        self.parser.set_defaults(__command=self)

    def add_sub_command(self, name: str, sub_command_class):
        if self.sub_parsers is None:
            self.sub_parsers = self.parser.add_subparsers()
        middlewares = [middleware() for middleware in sub_command_class.middlewares]
        sub_parser = self.sub_parsers.add_parser(name, parents=[middleware.parser for middleware in middlewares])
        obj = sub_command_class(sub_parser, middlewares)
        return obj

    def exec(self, args):
        for middleware in self.middlewares:
            middleware.exec(args, self.ctx)
