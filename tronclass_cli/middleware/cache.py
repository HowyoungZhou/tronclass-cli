from pathlib import Path

from tronclass_cli.middleware import Middleware
from tronclass_cli.utils.cache import Cache


class CacheMiddleware(Middleware):
    name = 'cache'

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--cache-dir', type=Path, default=self.default_root / 'dat')
        group.add_argument('--force-update', action='store_true')

    def _exec(self, args):
        args.cache_dir.mkdir(0o700, True, True)
        if 'cache' not in self._ctx:
            self._ctx.cache = Cache(args.cache_dir / 'cache', args.force_update)

    def _dispose(self):
        self._ctx.cache.close()
