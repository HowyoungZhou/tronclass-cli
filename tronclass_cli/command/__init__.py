from argparse import ArgumentParser


class Command:
    name = None

    def __init__(self, parser: ArgumentParser):
        self.parser = parser
        self.sub_parsers = None
        self.init_parser()

    def init_parser(self):
        self.parser.set_defaults(__command=self)

    def add_sub_command(self, name: str, sub_command_class):
        if self.sub_parsers is None:
            self.sub_parsers = self.parser.add_subparsers()
        sub_parser = self.sub_parsers.add_parser(name)
        obj = sub_command_class(sub_parser)
        return obj

    def sub_command(self, name):
        def sub_command_decorator(sub_command_class):
            self.add_sub_command(name, sub_command_class)
            return sub_command_class

        return sub_command_decorator
