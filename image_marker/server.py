# -*- coding: utf-8 -*-
import logging
import pkg_resources
import json

from os import path, getcwd
from urllib.parse import urlparse

import tornado
import tornado.ioloop
import tornado.web

from .storage import Markers


UPLOADS = 'uploads'


class LandingPage(tornado.web.RequestHandler):
    def get(self):
        with open(path.join('/var/imarker/web/index.html'), 'rb') as f:
            self.set_header('Content-type', 'text/html')
            self.write(f.read())


class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        dst = path.join(getcwd(), UPLOADS, fname)
        with open(dst, 'wb') as f:
            f.write(fileinfo['body'])
        self.finish('{} is uploaded to {} folder'.format(fname, dst))


class Sample(tornado.web.RequestHandler):

    markers = None

    def post(self):
        if not Sample.markers:
            LandingPage.markers = Markers('./marks')
        data = self.request.body
        print('received: {}'.format(data))
        data = json.loads(data)
        parts = self.path.selfplit('/')
        Sample.markers.process_image(
            image=data['image'],
            organ=parts[2],
            area=data['area'],
        )
        self.send_preamble()
        self.write('1')


application = tornado.web.Application(
    handlers=[
        (r'/', LandingPage),
        (r'/file-upload', Upload),
    ],
    static_path='/var/imarker/web/',
    debug=True)
