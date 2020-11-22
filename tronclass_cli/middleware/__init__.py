from argparse import ArgumentParser

from tronclass_cli.config import config


class Context:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if not isinstance(other, Context):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        return f'{self.__class__.__qualname__}({", ".join([f"{k} = {v}" for k, v in self.__dict__.items()])})'


class Middleware:
    name = None
    middleware_classes = []

    def __init__(self, parser: ArgumentParser, ctx: Context):
        self._parser = parser
        self._ctx = ctx
        self._middlewares = [middleware_class(parser, ctx) for middleware_class in self.middleware_classes]
        self.init_parser()

    def init_parser(self):
        self._init_parser()
        self._parser.set_defaults(__middleware=self, **config.get_section(self.name).to_dict())

    def _init_parser(self):
        pass

    def exec(self, args):
        for middleware in self._middlewares:
            middleware.exec(args)
        self._exec(args)

    def _exec(self, args):
        pass
