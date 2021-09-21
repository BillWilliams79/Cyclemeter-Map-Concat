#
# imports
#
import numpy as np
#import pandas as pd
import re as re
from jinja2 import Environment, FileSystemLoader

import gps_transform




#
# file handling
#
fileName = input('Enter name of GPX file : ')
fileHandle = open(fileName)
GPS_POINT_DELTA = int(input('Enter minimum distance between GPS points in meters : '))
etl_name = 'Strava GPX %dm delta' % (GPS_POINT_DELTA)

count = 0
dataList = list()
latCount = 0
lonCount = 0
eleCount = 0
gpsTimeCount = 0

#
# commence parsing the metadata section first before parsing the GPS points
#
for line in fileHandle:

    if len(re.findall('</metadata>', line)) > 0:
        # metadata end tag, stop processing.
        break
    else:
        continue

#
# process file line by line looking for track points and eleveation data.
# these three values consume two lines in gpx files with elevation
# on the secone line. So lat/lon are collected first and then
# the data is stuffed into a list of dictionaries
#
for line in fileHandle:
    #
    # regular expression method of finding values
    #
    lat = re.findall('lat="([0-9.-]+)', line)
    if lat != []:
       dataList.append(dict({'latitude' : lat[0]}))
       latCount += 1

    lon = re.findall('lon="([0-9.-]+)', line)
    if lon != []:
        dataList[len(dataList) - 1]['longitude'] = lon[0]
        lonCount += 1

    ele = re.findall('<ele>([0-9.-]+)', line)
    if ele != []:
        dataList[len(dataList) - 1]['elevation'] = ele[0]
        eleCount += 1

    gpsTime = re.findall('<time>([0-9.\-:T]+)', line)
    if gpsTime != []:
        dataList[len(dataList) - 1]['gpstime'] = gpsTime[0]
        gpsTimeCount += 1
      
        #this debug code breaks the ingest points processing after 5 gps points
        #count = count + 1
        #if count == 5:
            #print(dataList)
        #    break        

imported_points = len(dataList)
print('\nGPS points imported\t\t: %d' % imported_points)



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
