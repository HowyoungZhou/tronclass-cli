import os
import pickle
import stat
from getpass import getpass

from tronclass_cli import config
from tronclass_cli.api.auth.providers import get_auth_provider
from tronclass_cli.middleware import Middleware
from tronclass_cli.utils import interact


def login(user_id):
    auth_provider_class = get_auth_provider(config.provider)
    interact.prompt(f'🔐 Login with your {auth_provider_class.desc} account')
    user_id = interact.prompt_input('User ID', user_id)
    password = getpass()
    auth_provider = auth_provider_class()
    session = auth_provider.login(user_id, password)
    config.sessions_dir.mkdir(0o700, True, True)
    session_file = config.sessions_dir / f'{user_id}-{config.provider}.session'
    with open(session_file, 'wb') as fs:
        os.chmod(session_file, stat.S_IRUSR | stat.S_IWUSR)
        pickle.dump(session, fs)
    return session


class SessionMiddleware(Middleware):
    name = 'session'

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--user-id', help='user id used to login')

    def _exec(self, args):
        session_files = config.sessions_dir.glob(
            f'{args.user_id}-{config.provider}.session' if args.user_id is not None else f'*-{config.provider}.session')
        session_files = list(session_files)
        if len(session_files) > 0:
            with open(session_files[0], 'rb') as fs:
                self._ctx.session = pickle.load(fs)
        else:
            self._ctx.session = login(args.user_id)
