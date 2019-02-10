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

from .storage import Markers
from .texture import Extractor, Marker


def project():
    return __name__.split('.')[-2]


class LandingPage(tornado.web.RequestHandler):
    def get(self):
        index = path.join(prefix, 'var/{}/web/index.html'.format(project()))
        with open(index, 'rb') as f:
            self.set_header('Content-type', 'text/html')
            self.write(f.read())


class Upload(tornado.web.RequestHandler):

    extractor = Extractor('./uploads')

    def post(self):
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        uploads = path.join(prefix, 'var/{}/web/uploads'.format(project()))
        pathlib.Path(uploads).mkdir(parents=True, exist_ok=True)
        dst = path.join(uploads, fname)

        with open(dst, 'wb') as f:
            f.write(fileinfo['body'])

        uploaded = Upload.extractor.extract(dst)
        uploaded = path.relpath(uploaded, uploads)
        self.finish(json.dumps(path.join('static/uploads', uploaded)))


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
        image = path.join(prefix, 'var/{}/web/uploads'.format(project()), *(args[2:]))
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
        (r'/file-upload', Upload),
        (r'/images/.*', Images),
        (r'/sample/.*', Sample),
    ],
    static_path=path.join(prefix, 'var/{}/web/'.format(project())),
    debug=True)
