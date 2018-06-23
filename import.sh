#!/usr/bin/evn bash

set -ex
imarker-csv --when $(date +%d%m%Y --date='2 weeks ago') ../t2-t1/texture-stats-makeda-0.csv
imarker-csv --when $(date +%d%m%Y --date='1 week ago') ../t2-t1/texture-stats-makeda-1.csv
imarker-csv --when $(date +%d%m%Y --date='2 weeks ago') ../t2-t1/texture-stats-other-guy-0.csv
imarker-csv --when $(date +%d%m%Y --date='1 week ago') ../t2-t1/texture-stats-other-guy-1.csv
