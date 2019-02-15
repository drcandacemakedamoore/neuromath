# -*- coding: utf-8 -*-

import logging


aboindex_2d = {
    'swatches': [
        {
            'name': 'lesion',
            'title': 'Lesion Area',
            'color': '#fdb827',
        },
        {
            'name': 'liver',
            'title': 'Liver Area',
            'color': '#61bb46',
        },
        {
            'name': 'bone',
            'title': 'Bone Area',
            'color': '#3e3d97',
        },
        {
            'name': 'fat',
            'title': 'Fat Area',
            'color': '#ee1f98',
        },
        {
            'name': 'lung',
            'title': 'Lung Area',
            'color': '#3d7a97',
        },
        {
            'name': 'kidney',
            'title': 'Kidney Area',
            'color': '#2804cc',
        },
        {
            'name': 'psoas-muscle',
            'title': 'Psoas Muscle',
            'color': '#f5821f',
        },
        {
            'name': 'other-muscle',
            'title': 'Other Muscle',
            'color': '#04b8cf',
        },
        {
            'name': 'spleen',
            'title': 'Spleen',
            'color': '#e03a3a',
        },
        {
            'name': 'other-r-o-i',
            'title': 'Other-r-o-i',
            'color': '#c2cf04',
        },
        {
            'name': 'bowel',
            'title': 'Bowel',
            'color': '#963d97',
        },
    ],
}


class Models:

    def for_page(self, page):
        logging.info('Requesting model for page: {}'.format(page))
        if page.endswith('2dabdoindex.html'):
            return aboindex_2d
