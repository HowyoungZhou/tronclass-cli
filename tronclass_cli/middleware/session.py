from datetime import timedelta
from getpass import getpass
from pathlib import Path

import keyring

from tronclass_cli.api.auth.providers import get_auth_provider, get_all_auth_providers
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
        group.add_argument('--username', help='username for authentication')
        group.add_argument('--auth-provider', default='zju',
                           help=f'authentication provider, available providers: {", ".join(get_all_auth_providers().keys())}')
        group.add_argument('--no-save-credentials', dest='save_credentials', action='store_false',
                           help='do not save the credentials')

    def _exec(self, args):
        username = args.username or interact.prompt_input('Username')
        self._ctx.username = username
        self._ctx.session = self._ctx.cache.get(f'session.{username}')
        if self._ctx.session is not None:
            return
        password = keyring.get_password(SERVICE_NAME, username) or getpass()
        if args.save_credentials:
            keyring.set_password(SERVICE_NAME, username, password)
        auth_provider = get_auth_provider(args.auth_provider)()
        self._ctx.session = auth_provider.login(username, password)
        self._ctx.cache.set(f'session.{username}', self._ctx.session, SESSION_LIFETIME)
