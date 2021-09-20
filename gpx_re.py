#
# imports
#
import numpy as np
import pandas as pd
import re as re
from jinja2 import Environment, FileSystemLoader
from geopy import distance
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
    #cleanLine = line.lstrip()

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



gps_distance = list()
count = 0
points_stripped = 0
for index, gps_point in enumerate(dataList):
    
    current_point = (gps_point['latitude'], gps_point['longitude'])

    while True:
        if index == len(dataList) - 1:
            # break loop when last element detected
            #print(count)
            break

        next_point = (dataList[index+1]['latitude'], dataList[index+1]['longitude'])
        mydistance = distance.distance(current_point, next_point)
    
        if round(mydistance.m,1) < GPS_POINT_DELTA:
            dataList.pop(index+1)
            points_stripped += 1
            continue
        else:
            gps_distance.append(round(mydistance.m, 1))    
            count += 1
            #break the while
            break
    #
    # debug code prints lat/lon and delta for points
    #
    #if index == 0:
    #    print("\npoint 0 lat lon : %s %s\npoint 1 lat lon : %s %s\ndistance (m) : %f\n" % 
    #            (gps_point['latitude'], gps_point['longitude'], dataList[index+1]['latitude'], dataList[index+1]['longitude'], round(mydistance.m, 1)))



#print(gps_distance) 
print('GPS points stripped @ %dm\t: %d' % (GPS_POINT_DELTA, points_stripped))  
print('GPS points after distance strip\t: %d' % (len(dataList)))
percent_reduction = round(100 * (points_stripped / imported_points), 1)

print('GPS points reduced %g percent' % (percent_reduction))  
points_df = pd.DataFrame(gps_distance, index=None, columns=['Distance'])
#print(points_df)
print('\nMean\t: %f\nMedian\t: %f\nMin\t: %f\nMax\t: %f' % (points_df.mean(), points_df.median(), points_df.min(), points_df.max()))




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



#
# instantiate, print and then write to file in CSV format
#
#print(dataList)
#myDataFrame = pd.DataFrame(dataList, index = None, columns = ['latitude', 'longitude', 'elevation', 'gpstime'])

#print(myDataFrame)
#print(myDataFrame.size)

#print(latCount, lonCount, eleCount, gpsTimeCount)

#myDataFrame.to_csv('temp.csv')

#  geodesic()


print('the end')
