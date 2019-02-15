# -*- coding: utf-8 -*-
import logging
import json
import pathlib

from os import path, scandir
from sys import prefix
from glob import glob

import tornado
import tornado.ioloop
import tornado.web

from jinja2 import Template, Undefined

from .storage import Markers
from .texture import Extractor, Marker
from .models import Models


class AllowEmpty(Undefined):

    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
        __float__ = __complex__ = __pow__ = __rpow__ = \
        _fail_with_undefined_error


def project():
    return __name__.split('.')[-2]


class LandingPage(tornado.web.RequestHandler):

    def get(self):
        index = path.join(prefix, 'var', project(), 'web/index.html')
        with open(index, 'rb') as f:
            self.set_header('Content-type', 'text/html')
            self.write(f.read())


class Templates:

    def for_page(self, page):
        return path.join(
            prefix,
            'var',
            project(),
            'web/templates/section.html',
        )


class Sections(tornado.web.RequestHandler):

    models = Models()
    templates = Templates()

    def get(self):
        tpl_path = self.templates.for_page(self.request.path)
        with open(tpl_path, 'r') as tpl_body:
            tpl = Template(tpl_body.read(), undefined=AllowEmpty)
            self.set_header('Content-type', 'text/html')
            model = self.models.for_page(self.request.path)
            self.write(tpl.render(**model))


class Upload(tornado.web.RequestHandler):

    extractor = Extractor('./uploads')

    def post(self):
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        uploads = path.join(prefix, 'var', project(), 'web/uploads')
        pathlib.Path(uploads).mkdir(parents=True, exist_ok=True)
        dst = path.join(uploads, fname)

        with open(dst, 'wb') as f:
            f.write(fileinfo['body'])

        uploaded = Upload.extractor.extract(dst)
        uploaded = path.relpath(uploaded, uploads)
        self.finish(json.dumps(path.join('/static/uploads', uploaded)))


class Sample(tornado.web.RequestHandler):

    markers = Markers('./marks')

    def save_image(self, organ):
        data = json.loads(self.request.body)
        logging.info('received: {}'.format(data))
        Sample.markers.process_image(
            image=data['image'],
            organ=organ[0],
            area=data['area'],
        )
        self.send_preamble()
        self.write('1')

    def sample_image(self, args):
        data = json.loads(self.request.body)
        area = [int(x) for x in data['area']]
        image = path.join(prefix, 'var', project(), 'web/uploads', *(args[2:]))
        marker = Marker(image, area, None)
        patch = marker.extract_patch(area[:2], area[2:])
        stats = [float(x) for x in marker.texture_stats(patch)]
        self.write(json.dumps(stats))

    def post(self):
        parts = [p for p in self.request.path.split('/') if p]
        first = parts.pop(0)
        first = parts.pop(0)
        if first == 'save':
            self.save_image(parts)
        elif first == 'tag':
            self.sample_image(parts)


class Images(tornado.web.RequestHandler):

    def list_subdirectories(self, subdir, id):
        top = path.basename(subdir)
        children = []
        result = {
            'text': top,
            'children': children,
            'id': id[0],
        }
        if path.isdir(subdir):
            for entry in scandir(subdir):
                id[0] = id[0] + 1
                if entry.is_dir():
                    children.append(self.list_subdirectories(entry.path, id))
                else:
                    children.append({
                        'text': entry.name,
                        'id': id[0],
                        'icon': 'jstree-file',
                    })
        return result

    def get(self):
        cmd = self.request.path.split('/')[2]
        logging.info('images command: {}'.format(cmd))
        if cmd == 'list':
            samples = path.join(prefix, 'var/{}/web/uploads/samples'.format(project()))
            logging.info('looing for images in {}/**/*.png'.format(samples))
            found = glob(samples + '/**/*.png', recursive=True)
            found = [f[len(samples) + 1:] for f in found]
            self.write(json.dumps(found))
        elif cmd == 'tree':
            samples = path.join(prefix, 'var/{}/web/uploads/samples'.format(project()))
            id = [0]
            result = self.list_subdirectories(samples, id)
            result['state'] = {'opened': True}
            self.write(json.dumps([result]))


application = tornado.web.Application(
    handlers=[
        (r'/', LandingPage),
        (r'/sections/.*', Sections),
        (r'/file-upload', Upload),
        (r'/images/.*', Images),
        (r'/sample/.*', Sample),
    ],
    static_path=path.join(prefix, 'var', project(), 'web'),
    debug=True,
)
