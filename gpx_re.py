#
# imports
#
import numpy as np

import re as re
from jinja2 import Environment, FileSystemLoader

import gps_transform, gps_extract

#
# User Input
#
fileName = input('Enter name of GPX file : ')
GPS_POINT_DELTA = int(input('Enter minimum distance between GPS points in meters : '))
etl_name = 'Strava GPX %dm delta' % (GPS_POINT_DELTA)
dataList = list()

#
# GPS Extract
#
gps_extract.gpx_file_extract(fileName, dataList)


#
# GPS Transforms
#
gps_transform.distance_optimizer(dataList, GPS_POINT_DELTA)
gps_transform.precision_optimizer(dataList, 2)

#
# Now store gps points in strava gpx file using Jinja2
#
file_loader = FileSystemLoader('Templates')
Env = Environment(loader=file_loader, trim_blocks=True)

template = Env.get_template('child.txt')


handle = open(etl_name.lower() + ".gpx", "w")
handle.write(template.render(ride_title = etl_name, gps_list = dataList))
handle.close()


print('the end')
