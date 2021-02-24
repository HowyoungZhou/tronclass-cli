import shutil

from tronclass_cli.command import Command
from tronclass_cli.middleware.cache import CacheMiddleware


class CacheCommand(Command):
    name = 'cache'

    def _exec(self, args):
        self._parser.print_help()


class CacheClearCommand(Command):
    name = 'cache.clear'
    middleware_classes = [CacheMiddleware]

    def _init_parser(self):
        pass

    def _exec(self, args):
        shutil.rmtree(args.cache_dir)
