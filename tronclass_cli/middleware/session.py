from datetime import timedelta
from getpass import getpass
from pathlib import Path

import keyring

from tronclass_cli.api.auth.providers import get_auth_provider
from tronclass_cli.middleware import Middleware
from tronclass_cli.middleware.cache import CacheMiddleware
from tronclass_cli.utils import interact

SERVICE_NAME = 'tronclass'
SESSION_LIFETIME = timedelta(hours=1)


class SessionMiddleware(Middleware):
    name = 'session'
    middleware_classes = [CacheMiddleware]

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--user-id', help='user id used to login')
        group.add_argument('--provider', default='zju')
        group.add_argument('--no-save-credentials', dest='save_credentials', action='store_false')
        group.add_argument('--session-dir', type=Path, default=self.default_root / 'sessions')

    def _exec(self, args):
        user_id = args.user_id or interact.prompt_input('User ID')
        self._ctx.user_name = user_id
        self._ctx.session = self._ctx.cache.get(f'session.{user_id}')
        if self._ctx.session is not None:
            return
        password = keyring.get_password(SERVICE_NAME, user_id) or getpass()
        if args.save_credentials:
            keyring.set_password(SERVICE_NAME, user_id, password)
        auth_provider = get_auth_provider(args.provider)()
        self._ctx.session = auth_provider.login(user_id, password)
        self._ctx.cache.set(f'session.{user_id}', self._ctx.session)
