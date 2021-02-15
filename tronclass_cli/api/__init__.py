import json
from functools import reduce
from urllib.parse import urljoin

from requests import Session
from bs4 import BeautifulSoup


def url_join(*urls):
    return reduce(urljoin, urls)


class Api:
    def __init__(self, base_url, session=Session()):
        self._base_url = base_url
        self._session = session

    def get_api_url(self, path):
        return urljoin(self._base_url, path)

    def get_todo(self):
        return self._session.get(self.get_api_url('api/todos')).json()['todo_list']

    def get_user_id(self):
        return 56159
        html = self._session.get(self.get_api_url('user/index')).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find(id='userId').get('value')

    def get_courses(self, conditions={}, fields='id,name', page_size=20):
        user_id = self.get_user_id()
        page = 1
        while True:
            params = {
                'conditions': json.dumps(conditions),
                'fields': fields,
                'page': page,
                'page_size': page_size
            }
            res = self._session.get(self.get_api_url(f'api/users/{user_id}/courses'), params=params)
            res.raise_for_status()
            data = res.json()
            yield from data['courses']

            if page >= data['pages']:
                break
            page += 1

    def get_homework(self, course_id, conditions={}, page_size=20):
        page = 1
        while True:
            params = {
                'conditions': json.dumps(conditions),
                'page': page,
                'page_size': page_size
            }
            res = self._session.get(self.get_api_url(f'api/courses/{course_id}/homework-activities'), params=params)
            res.raise_for_status()
            data = res.json()
            yield from data['homework_activities']

            if page >= data['pages']:
                break
            page += 1
