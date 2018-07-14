#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

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
        '/var/imarker/web': [
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
        ('/opt/conda/bin', ['bin/imarker']),
        ('/var/imarker/web', [
            'web/index.html',
        ]),
        ('/var/imarker/web/js', [
            'web/js/bootstrap.bundle.min.js',
            'web/js/bootstrap.bundle.min.js.map',
            'web/js/jquery-3.3.1.min.js',
            'web/js/svg.min.js',
            'web/js/dropzone.js',
            'web/js/tagger.js',
        ]),
        ('/var/imarker/web/css', [
            'web/css/bootstrap.min.css',
            'web/css/bootstrap.min.css.map',
        ]),
        ('/var/imarker/web/img', [
            'web/img/t1.png',
        ])
    ],
    install_requires=[
        'pandas >= 0.23.1',
        'numpy >= 1.14.5',
        'Pillow >= 5.1.0',
        'scipy >= 1.1.0',
        'scikit-image >= 0.14.0',
        # 'pywebview >= 2.0.3',
        # 'pywebview[qt5];platform_system=="Linux"',
        # 'pywebview[winforms];platform_system=="Windows"',
        # 'pywebview[cocoa];platform_system=="Darwin"',
        # 'vext >= 0.7.0',
        # 'vext.gi >= 0.7.0',
        'sqlalchemy >= 1.2.8',
        'tornado >= 5.0.2',
    ],
    tests_require=[
        'pytest >= 3.4.2',
    ],
    # extras_require=[],
)
