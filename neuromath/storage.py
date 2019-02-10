# -*- coding: utf-8 -*-

import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Date,
    String,
    Float,
)
from time import time

from .texture import Marker


class Markers:

    engine = create_engine('sqlite:///marked_images.db', echo=False)
    marked_images = 'marked_images'

    if not engine.dialect.has_table(engine, marked_images):
        metadata = MetaData(engine)
        Table(
            marked_images,
            metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('image', String),
            Column('date', Date),
            Column('sample', String),
            Column('std', Float),
            Column('entropy', Float),
            Column('dissimilarity', Float),
            Column('correlation', Float),
            Column('x', Integer),
            Column('y', Integer),
            Column('width', Integer),
            Column('height', Integer),
            sqlite_autoincrement=True,
        )
        metadata.create_all()

    def __init__(self, marked_dir):
        self.marked_dir = marked_dir

    def process_image(self, image, organ, area):
        marker = Marker(image, area, self.marked_dir)
        df = marker.mark()
        df['date'] = time()
        df['sample'] = organ
        self.to_sql(df)

    def import_csv(self, incsv, when):
        df = pd.read_csv(incsv, index_col=False)
        df['sample'] = df['sample'].map({
            'leison_one': 'lesion',
            'leison_two': 'lesion',
            'liver_one': 'liver',
            'liver_two': 'liver',
            'spleen': 'spleen',
            'soft_tissue_one': 'soft_tissue',
            'soft_tissue_two': 'soft_tissue',
            'bowels': 'bowels',
        })
        df['date'] = when
        self.to_sql(df)

    def to_sql(self, df):
        df.to_sql(
            Markers.marked_images,
            Markers.engine,
            if_exists='append',
            index=False,
        )
