import os
from glob import glob
from itertools import chain
from tempfile import TemporaryFile
from zipfile import ZipFile

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from tronclass_cli.api import Api
from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware


def zip_files(fp, paths):
    with ZipFile(fp, 'w') as zf:
        for path in paths:
            path = os.path.normpath(path)
            if os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for name in sorted(dirnames):
                        path = os.path.normpath(os.path.join(dirpath, name))
                        zf.write(path, path)
                    for name in filenames:
                        path = os.path.normpath(os.path.join(dirpath, name))
                        if os.path.isfile(path):
                            zf.write(path, path)
            else:
                zf.write(path)


def post_file(api: Api, name, fp):
    fp.seek(0, 2)
    file_size = fp.tell()
    fp.seek(0, 0)

    upload = api.post_uploads(name, file_size)

    progress_bar = None

    def update_callback(monitor):
        progress_bar.n = monitor.bytes_read
        progress_bar.refresh()

    data = MultipartEncoder(
        fields={'file': (name, fp)}
    )
    monitor = MultipartEncoderMonitor(data, update_callback)
    progress_bar = tqdm(desc=name, total=data.len, unit='iB', unit_scale=True)
    headers = {'Content-Type': monitor.content_type, 'Content-Length': str(data.len)}
    res = api.session.put(upload['upload_url'], data=monitor, headers=headers)

    if progress_bar.n != data.len:
        raise IOError('file size mismatches')
    progress_bar.close()
    res.raise_for_status()
    return upload['id']


class HomeworkSubmitCommand(Command):
    name = 'courses.submit'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('activity_id', help='homework activity id')
        self._parser.add_argument('paths', nargs='+', type=glob,
                                  help='files or directories to be submitted, glob supported')
        self._parser.add_argument('--compress', metavar='NAME', help='compress the files with given file name')
        self._parser.add_argument('--draft', action='store_true', help='submit as a draft')

    def _exec(self, args):
        self._ctx.api.get_activity(args.activity_id)
        paths = chain(*args.paths)
        uploads = []
        if args.compress is not None:
            with TemporaryFile() as fp:
                zip_files(fp, paths)
                uploads.append(post_file(self._ctx.api, args.compress, fp))
        else:
            for path in paths:
                if not os.path.isfile(path):
                    raise TypeError('folders are not supported to be uploaded, use --compress to create a zipped file')
                with open(path, 'rb') as fp:
                    uploads.append(post_file(self._ctx.api, os.path.basename(path), fp))
        self._ctx.api.post_submissions(args.activity_id, uploads, is_draft=args.draft)
