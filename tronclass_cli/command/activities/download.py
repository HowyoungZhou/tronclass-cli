from pathlib import Path

from tqdm import tqdm

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware


class ActivitiesDownloadCommand(Command):
    name = 'activities.download'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('reference_id', help='reference id of the file')
        self._parser.add_argument('output_file', type=Path, help='path to the output file')
        self._parser.add_argument('--preview', action='store_true', help='download the preview file')

    def _exec(self, args):
        res = self._ctx.api.get_document(args.reference_id, args.preview)
        total_size = int(res.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_file, 'wb') as fs:
            for data in res.iter_content(block_size):
                progress_bar.update(len(data))
                fs.write(data)
        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            raise IOError('file size mismatches')
