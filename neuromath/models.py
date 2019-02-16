# -*- coding: utf-8 -*-

import logging

from collections import namedtuple


Swatch = namedtuple('Swatch', ['name', 'color'])


brainindex_2d = {
    'swatches': [
        { 
            'name': 'pineal',
            'color': '61bb46',
        },
        {
            'name': 'lesion',
        },
        {
            'name': 'lesion',
            'title': 'Lesion Area',
            'color': '#fdb827',
        },
        {
            'name': 'hypothalamus',
            'title': 'Hypothalamus',
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
            'name': 'pineal',
            'title': 'Pineal Area',
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




abdoindex_2d = {
    'swatches': [
        Swatch('lesion','#fdb827'),
        Swatch('liver','#61bb46'),
        Swatch('bone','#3e3d97'),
        Swatch('fat','#ee1f98'),
        Swatch('lung','#3d7a97'),
        Swatch('kidney','#2804cc'),
        Swatch('psoas-muscle','#f5821f'),
        Swatch('other-muscle','#04b8cf'),
        Swatch('spleen','#e03a3a'),
        Swatch('other-r-o-i','#c2cf04'),
        Swatch('bowel','#963d97'),
    ],
}

brainindex_2d = {
    'swatches': [
        Swatch('pineal', '#61bb46'),
        Swatch('lesion', '#fdb827'),
        Swatch('medulla', '#f5821f'),
        Swatch('midbrain', '#04b8cf'),
        Swatch('cystinside', '#c2cf04'),
        Swatch('potentialinfarctingarea', '#2804cc'),
        Swatch('infarctedarea', '#e03a3a'),
        Swatch('leftthalamus', '#963d97'),
        Swatch('hippocampus', '#3d7a97'),
        Swatch('hematoma', '#3e3d97'),
        Swatch('righthypothalamus', '#ee1f98'),
    ]
}

freelabel_2d = {
    'swatches': [
        Swatch('a', '#61bb46'),
        Swatch('lesion', '#fdb827'),
        Swatch('b', '#f5821f'),
        Swatch('c', '#04b8cf'),
        Swatch('other-r-o-i', '#c2cf04'),
        Swatch('d', '#2804cc'),
        Swatch('j', '#e03a3a'),
        Swatch('h', '#963d97'),
        Swatch('e', '#3d7a97'),
        Swatch('f', '#3e3d97'),
        Swatch('i', '#ee1f98'),
    ]
}

headandneck_2d = {
    'swatches': [
        Swatch('thyroid', '#61bb46'),
        Swatch('lesion', '#fdb827'),
        Swatch('cystinside', '#5c4d61'),
        Swatch('muscle', '#f5821f'),
        Swatch('thymus', '#04b8cf'),
        Swatch('other-r-o-i', '#c2cf04'),
        Swatch('trachea', '#2804cc'),
        Swatch('left-parotid', '#e03a3a'),
        Swatch('right-parotid', '#963d97'),
        Swatch('lymph-node', '#3d7a97'),
        Swatch('bone', '#3e3d97'),
        Swatch('fat', '#ee1f98'),
    ]
}

mskidnex_2d = {
    'swatches': [
        Swatch('tendon', '#61bb46'),
        Swatch('lesion', '#fdb827'),
        Swatch('epiphysisofbone', '#f5821f'),
        Swatch('muscle-a-right', '#04b8cf'),
        Swatch('muscle-a-left', '#0e2124'),
        Swatch('muscle-b-right', '#100411'),
        Swatch('muscle-b-left', '#04cf7a'),
        Swatch('other-r-o-i', '#c2cf04'),
        Swatch('ligament', '#2804cc'),
        Swatch('cancellous-bone', '#e03a3a'),
        Swatch('cortical-bone', '#963d97'),
        Swatch('metaphysis', '#3d7a97'),
        Swatch('diaphysis', '#3e3d97'),
        Swatch('fat', '#ee1f98'),
    ]
}

thorax_2d = {
    'swatches': [
        Swatch('thymus', '#61bb46'),
        Swatch('lesion', '#fdb827'),
        Swatch('heart-muscle', '#f5821f'),
        Swatch('other-muscle', '#04b8cf'),
        Swatch('other-r-o-i', '#c2cf04'),
        Swatch('thyroid', '#2804cc'),
        Swatch('greatvessel', '#e03a3a'),
        Swatch('heart', '#963d97'),
        Swatch('lung', '#3d7a97'),
        Swatch('bone', '#3e3d97'),
        Swatch('fat', '#ee1f98'),
    ]
}


class Models:

    def for_page(self, page):
        logging.info('Requesting model for page: {}'.format(page))
        if page.endswith('/2dabdoindex.html'):
            return aboindex_2d
        if page.endswith('/2dbrainindex.html'):
            return brainindex_2d
        if page.endswith('/2dfreelabel.html'):
            return freelabel_2d
        if page.endswith('/2dheadandneckindex.html'):
            return headandneck_2d
        if page.endswith('/2dmskindex.html'):
            return mskidnex_2d
        if page.endswith('/2dthoraxindex.html'):
            return thorax_2d
