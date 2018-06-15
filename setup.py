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
    scripts=['bin/imarker'],
    package_data={
        'image_marker/web': [
            'web/*.html',
            'web/*.js',
            'web/*/*.js',
            'web/*/*.js.map',
            'web/css/*.css',
            'web/css/*.css.map',
        ],
    },
    data_files=[
        ('image_marker/web', [
            'web/index.html',
            'web/tagger.js',
        ]),
        ('image_marker/web/js', [
            'web/js/bootstrap.min.js',
            'web/js/jquery-3.3.1.slim.min.js',
        ]),
        ('image_marker/web/css', [
            'web/css/bootstrap.min.css',
            'web/css/bootstrap.min.css.map',
        ]),
    ],
    install_requires=[
        'pytest >= 3.4.2',
    ],
)
