from datetime import timedelta
from getpass import getpass

import keyring
from requests import Session

from tronclass_cli.api.auth.providers import get_auth_provider, get_all_auth_providers
from tronclass_cli.middleware import Middleware
from tronclass_cli.middleware.cache import CacheMiddleware
from tronclass_cli.utils import interact

SERVICE_NAME = 'tronclass'
SESSION_LIFETIME = timedelta(hours=1)
DEFAULT_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'


def try_get_password(service_name, username):
    try:
        return keyring.get_password(service_name, username)
    except:
        return None


def try_set_password(service_name, username, password):
    try:
        keyring.set_password(service_name, username, password)
        return True
    except:
        return False


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
        group.add_argument('--user-agent', default=DEFAULT_UA, help='user agent sent with requests')

    def _exec(self, args):
        username = args.username or interact.prompt_input('Username')
        self._ctx.username = username
        self._ctx.session = self._ctx.cache.get(f'session.{username}')
        if self._ctx.session is not None:
            return
        password = try_get_password(SERVICE_NAME, username) or getpass()
        if args.save_credentials:
            try_set_password(SERVICE_NAME, username, password)

        session = Session()
        session.headers['User-Agent'] = args.user_agent
        auth_provider = get_auth_provider(args.auth_provider)(session)
        self._ctx.session = auth_provider.login(username, password)
        self._ctx.cache.set(f'session.{username}', self._ctx.session, SESSION_LIFETIME)
