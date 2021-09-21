#
# imports
#
import gps_transform, gps_extract, gps_load

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
# GPS load
#
gps_load.gpx_file_load(dataList, etl_name)

print('the end')
