# -*- coding: utf-8 -*-
import logging
import pkg_resources

from http.server import BaseHTTPRequestHandler
from os import path
from urllib.parse import urlparse


class LandingPage(BaseHTTPRequestHandler):

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

    def serve_static(self, file, mime):
        '''
        Serves static files with given mime-type.
        '''
        res = 'web/{}'.format(file)
        logging.info('Trying to serve: {}'.format(res))
        if pkg_resources.resource_exists(__name__, res):
            self.send_response(200)
            self.send_header('Content-type', mime)
            self.end_headers()
            self.wfile.write(pkg_resources.resource_string(__name__, res))
        else:
            self.send_error(404, 'File Not Found: {}'.format(res))

    def fail(self):
        '''
        Sends internal server error message.
        '''
        self.send_error(500, 'Don\'t know what to do with: %s' % self.path)

    def do_GET(self):
        '''
        Handles HTTP GET requests.
        '''
        url = urlparse(self.path)
        extension = path.splitext(url.path)[1] or '.html'
        if self.path == '/':
            self.serve_static('index.html', self.statics['.html'])
        elif extension.lower() in self.statics:
            self.serve_static(url.path[1:], self.statics[extension.lower()])
        else:
            self.fail()

    def send_preamble(self):
        '''
        Starts sending success message.
        '''
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        '''
        Hanles AJAX requests.
        '''
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
        if self.path == '/categories/get':
            self.send_preamble()
            self.wfile.write(str(self.tree))
        elif self.path == '/categories/put':
            self.tree.add(data)
            self.wfile.write(str(self.tree))
        else:
            self.fail()
