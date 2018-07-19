#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from sys import prefix
from os import path
from setuptools import setup


setup(
    packages=['image_marker'],
    name='image-marker',
    version='0.0.1',
    description='Tag areas of image',
    author='Oleg Sivokon',
    author_email='olegsivokon@gmail.com',
    url='TBD',
    license='MIT',
    package_data={
        path.join(prefix, 'var/imarker/web'): [
            'web/*.html',
            'web/*.js',
            'web/*/*.js',
            'web/*/*.js.map',
            'web/css/*.css',
            'web/css/*.css.map',
            'web/img/*.png',
        ],
    },
    data_files=[
        (path.join(prefix, 'bin'), ['bin/imarker']),
        (path.join(prefix, 'var/imarker/web'), [
            'web/index.html',
        ]),
        (path.join(prefix, 'var/imarker/web/js'), [
            'web/js/bootstrap.bundle.min.js',
            'web/js/bootstrap.bundle.min.js.map',
            'web/js/jquery-3.3.1.min.js',
            'web/js/svg.min.js',
            'web/js/dropzone.js',
            'web/js/datatables.min.js',
            'web/js/jquery.dataTables.min.js',
            'web/js/tagger.js',
        ]),
        (path.join(prefix, 'var/imarker/web/css'), [
            'web/css/bootstrap.min.css',
            'web/css/bootstrap.min.css.map',
            'web/css/datatables.min.css',
        ]),
        (path.join(prefix, 'var/imarker/web/img'), [
            'web/img/t1.png',
        ])
    ],
    install_requires=[
        'pandas >= 0.23.1',
        'numpy >= 1.14.5',
        'Pillow >= 5.1.0',
        'scipy >= 1.1.0',
        'scikit-image >= 0.14.0',
        'sqlalchemy >= 1.2.8',
        'tornado >= 5.0.2',
        'pydicom >= 1.1.0',
        'pydicom-ext >= 0.4.7',
        'pypng >= 0.0.18',
    ],
    tests_require=[
        'pytest >= 3.4.2',
    ],
    # extras_require=[],
)
