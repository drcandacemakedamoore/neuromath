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


class PkgResources(tornado.web.RequestHandler):

    statics = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.jpg': 'image/jpg',
        '.png': 'image/png',
        '.bmp': 'image/bmp',
        '.gif': 'image/gif',
        '.map': 'application/json',
    }

    def render_resource(self, res):
        logging.info('Trying to serve: {}'.format(res))
        ext = path.splitext(res)[1]
        mime = self.statics[ext]
        if pkg_resources.resource_exists(__name__, res):
            self.set_header('Content-type', mime)
            self.write(pkg_resources.resource_string(__name__, res))
        else:
            self.send_error(404, 'File Not Found: {}'.format(res))

    def get(self, *args):
        res = path.join('web', *args)
        self.render_resource(res)


class LandingPage(PkgResources):
    def get(self):
        self.render_resource('/web/index.html')


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


application = tornado.web.Application([
    (r'/', LandingPage),
    (r'/(js|css|img)/(.+)', PkgResources),
    (r'/file-upload', Upload),
], debug=True)
