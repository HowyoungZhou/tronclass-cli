# import os
# import pickle
# import stat
import keyring
from getpass import getpass
from pathlib import Path

from tronclass_cli.api.auth.providers import get_auth_provider
from tronclass_cli.middleware import Middleware
from tronclass_cli.utils import interact

SERVICE_NAME = 'tronclass'


# def get_password(user_id, save_credentials):
#     password = getpass()
#     if save_credentials:
#         keyring.set_password(SERVICE_NAME, user_id, password)
#     return password


# def login(provider, user_id, session_dir, save_credentials, load_credentials=True):
#     auth_provider_class = get_auth_provider(provider)
#     interact.prompt(f'🔐 Login with your {auth_provider_class.desc} account')
#     user_id = interact.prompt_input('User ID', user_id)
#     if load_credentials:
#         password = keyring.get_password(SERVICE_NAME, user_id) or get_password(user_id, save_credentials)
#     else:
#         password = get_password(user_id, save_credentials)
#     auth_provider = auth_provider_class()
#     session = auth_provider.login(user_id, password)
#     # session_dir.mkdir(0o700, True, True)
#     # session_file = session_dir / f'{provider}-{user_id}.session'
#     # with open(session_file, 'wb') as fs:
#     #     os.chmod(session_file, stat.S_IRUSR | stat.S_IWUSR)
#     #     pickle.dump(session, fs)
#     return session


class SessionMiddleware(Middleware):
    name = 'session'

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--user-id', help='user id used to login')
        group.add_argument('--provider', default='zju')
        group.add_argument('--no-save-credentials', dest='save_credentials', action='store_false')
        group.add_argument('--session-dir', type=Path, default=self.default_root / 'sessions')

    def _exec(self, args):
        # session_files = args.session_dir.glob(
        #     f'{args.provider}-{args.user_id}.session' if args.user_id is not None else f'{args.provider}-*.session')
        # session_files = list(session_files)
        # session_files_count = len(session_files)
        # if len(session_files) > 0:
        #     i = 0
        #     if session_files_count > 1:
        #         options = [file.stem for file in session_files]
        #         i = interact.select('Select a session:', options)
        #     with open(session_files[i], 'rb') as fs:
        #         self._ctx.session = pickle.load(fs)
        # else:
        #     self._ctx.session = login(args.provider, args.user_id, args.session_dir, args.save_credentials)
        user_id = args.user_id or interact.prompt_input('User ID')
        password = keyring.get_password(SERVICE_NAME, user_id) or getpass()
        if args.save_credentials:
            keyring.set_password(SERVICE_NAME, user_id, password)
        auth_provider = get_auth_provider(args.provider)()
        self._ctx.session = auth_provider.login(user_id, password)
