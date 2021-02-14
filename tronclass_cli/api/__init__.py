from functools import reduce
from urllib.parse import urljoin

from requests import Session


def url_join(*urls):
    return reduce(urljoin, urls)


class Api:
    def __init__(self, base_url, session=Session()):
        self._base_url = base_url
        self._session = session

    def get_api_url(self, *path):
        return url_join(self._base_url, f'api/{"/".join(path)}')

    def get_todo(self):
        return self._session.get(self.get_api_url('todos')).json()['todo_list']
