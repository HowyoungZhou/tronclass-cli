import inspect
import json
import shelve
from datetime import timedelta
from types import GeneratorType
from urllib.parse import urljoin

from requests import Session
from bs4 import BeautifulSoup


def cached(key, lifetime=None):
    def cache_decorator(func):
        def cached_func(*args, **kwargs):
            call_args = inspect.getcallargs(func, *args, **kwargs)
            self = call_args['self']
            cache_key = f'api.{self._username}.{key.format(**call_args)}'
            value = self._cache.get(cache_key)
            if value is not None:
                return value
            value = func(*args, **kwargs)
            if isinstance(value, GeneratorType):
                value = list(value)
            self._cache.set(cache_key, value, lifetime)
            return value

        return cached_func

    return cache_decorator


class Api:
    def __init__(self, base_url, username, cache, session: Session):
        self._base_url = base_url
        self._username = username
        self.session = session
        self._cache = cache

    def _get_api_url(self, path):
        return urljoin(self._base_url, path)

    def _api_call(self, path, method='GET', **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(method, self._get_api_url(path), **kwargs)

    @cached('todo', timedelta(hours=6))
    def get_todo(self):
        return self._api_call('api/todos').json()['todo_list']

    @cached('user_id')
    def get_user_id(self):
        html = self._api_call('user/index').content
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find(id='userId').get('value')

    def _get_pages(self, path, params, data_key, page_size=20):
        page = 1
        while True:
            params = {
                'page': page,
                'page_size': page_size,
                **params
            }
            res = self._api_call(path, params=params)
            res.raise_for_status()
            data = res.json()
            yield from data[data_key]

            if page >= data['pages']:
                break
            page += 1

    @cached('courses.{fields}.{conditions}', timedelta(days=1))
    def get_courses(self, conditions={}, fields='id,name'):
        user_id = self.get_user_id()
        params = {
            'conditions': json.dumps(conditions),
            'fields': fields,
        }
        return self._get_pages(f'api/users/{user_id}/courses', params, 'courses')

    @cached('homework.{course_id}.{conditions}', timedelta(hours=6))
    def get_homework(self, course_id, conditions={}):
        params = {
            'conditions': json.dumps(conditions),
        }
        return self._get_pages(f'api/courses/{course_id}/homework-activities', params, 'homework_activities')

    @cached('activities.{course_id}.{fields}', timedelta(hours=6))
    def get_activities(self, course_id, fields=''):
        params = {
            'fields': fields,
        } if fields != '' else None
        res = self._api_call(f'api/courses/{course_id}/activities', params=params)
        res.raise_for_status()
        return res.json()['activities']

    def get_activity(self, activity_id):
        res = self._api_call(f'api/activities/{activity_id}')
        res.raise_for_status()
        return res.json()

    def get_document(self, ref_id, preview=False):
        res = self._api_call(f'https://courses.zju.edu.cn/api/uploads/reference/document/{ref_id}/url',
                             params={'preview': str(preview).lower()})
        res.raise_for_status()
        url = res.json()['url']
        return self.session.get(url, stream=True)

    def post_uploads(self, name, size, parent_type=None, parent_id=0, is_scorm=False, is_wmpkg=False):
        data = {
            "name": name,
            "size": size,
            "parent_type": parent_type,
            "parent_id": parent_id,
            "is_scorm": is_scorm,
            "is_wmpkg": is_wmpkg
        }
        res = self._api_call(f'api/uploads', 'POST', json=data)
        res.raise_for_status()
        return res.json()

    def post_submissions(self, activity_id, uploads, slides=[], comment='', is_draft=False):
        data = {
            "comment": comment,
            "uploads": uploads,
            "slides": slides,
            "is_draft": is_draft
        }
        res = self._api_call(f'api/course/activities/{activity_id}/submissions', 'POST', json=data)
        res.raise_for_status()
        return res.json()
