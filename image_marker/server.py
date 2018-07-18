# -*- coding: utf-8 -*-
import logging
import json
import pathlib

from os import path
from sys import prefix
from glob import glob

import tornado
import tornado.ioloop
import tornado.web

from .storage import Markers
from .texture import Extractor


class LandingPage(tornado.web.RequestHandler):
    def get(self):
        with open(path.join(prefix, 'var/imarker/web/index.html'), 'rb') as f:
            self.set_header('Content-type', 'text/html')
            self.write(f.read())


class Upload(tornado.web.RequestHandler):

    extractor = Extractor('./uploads')

    def post(self):
        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        uploads = path.join(prefix, 'var/imarker/web/uploads')
        pathlib.Path(uploads).mkdir(parents=True, exist_ok=True)
        dst = path.join(uploads, fname)

        with open(dst, 'wb') as f:
            f.write(fileinfo['body'])

        Upload.extractor.extract(dst)
        self.finish('{} is uploaded to {} folder'.format(fname, dst))


class Sample(tornado.web.RequestHandler):

    markers = Markers('./marks')

    def post(self):
        data = self.request.body
        logging.info('received: {}'.format(data))
        data = json.loads(data)
        parts = self.request.path.split('/')
        Sample.markers.process_image(
            image=data['image'],
            organ=parts[2],
            area=data['area'],
        )
        self.send_preamble()
        self.write('1')


class Images(tornado.web.RequestHandler):

    def get(self):
        cmd = self.request.path.split('/')[2]
        logging.info('images command: {}'.format(cmd))
        if cmd == 'list':
            samples = path.join(prefix, 'var/imarker/web/uploads/samples')
            logging.info('looing for images in {}/**/*.png'.format(samples))
            found = glob(samples + '/**/*.png', recursive=True)
            found = [f[len(samples) + 1:] for f in found]
            self.write(json.dumps(found))


application = tornado.web.Application(
    handlers=[
        (r'/', LandingPage),
        (r'/file-upload', Upload),
        (r'/images/.*', Images),
    ],
    static_path=path.join(prefix, 'var/imarker/web/'),
    debug=True)
