# -*- mode: dockerfile -*-

from continuumio/anaconda3

expose 8888/tcp
expose 8080/tcp

copy ./image_marker /opt/image-marker/image_marker
copy ./bin /opt/image-marker/bin
copy ./web /opt/image-marker/web
copy ./MANIFEST.in /opt/image-marker
copy ./setup.py /opt/image-marker

run conda install 'pandas >= 0.23.1' \
    'numpy >= 1.14.5' \
    'Pillow >= 5.1.0' \
    'scipy >= 1.1.0' \
    'scikit-image >= 0.14.0' \
    'sqlalchemy >= 1.2.8' \
    'tornado >= 5.0.2'

run conda install -c conda-forge gdcm 

run mkdir /var/imarker && \
    cd /opt/image-marker && \
    python setup.py install

cmd imarker
