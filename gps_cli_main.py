#
# imports
#
import gps_transform, gps_extract, gps_load

#
# Data structures
#
gpx_etl_op = dict()
gps_points = list()
gpx_etl_op["gps_points"] = gps_points
#
# initilize counters to zero
#
gpx_etl_op["imported_points"] = 0
gpx_etl_op["delta_points_stripped"] = 0
gpx_etl_op["current_points"] = 0

#
# User Input
#
gpx_etl_op["extract_file_name"] = input('Enter name of GPX file : ')
gpx_etl_op["gps_min_delta"] = int(input('Enter minimum distance between GPS points in meters : '))
gpx_etl_op["gps_precision_reduction"] = 2
gpx_etl_op["load_file_name"] = 'Strava GPX {gps_min_delta}m delta'.format(**gpx_etl_op)

#
# GPS Extract
#
gps_extract.gpx_file_extract(gpx_etl_op)

print('\nGPS Points extracted\t\t: {imported_points} (file: {extract_file_name})'.format(**gpx_etl_op))

#
# GPS Transform
#
gps_transform.distance_optimizer(gpx_etl_op)
gps_transform.precision_optimizer(gpx_etl_op)

print('GPS points stripped @ {gps_min_delta}m\t: {delta_points_stripped}'.format(**gpx_etl_op))  
print('GPS points after distance strip\t: {delta_points_stripped}'.format(**gpx_etl_op))
percent_reduction = round(100 * (gpx_etl_op["delta_points_stripped"] / gpx_etl_op["imported_points"]), 1)
print('GPS points reduced %g percent' % (percent_reduction))  

#
# GPS load
#
gps_load.gpx_file_load(gpx_etl_op)

#
# Print the items in the main dictionary for debug purposes
# Skipping the list of points of course
#
print(' ')
for item in gpx_etl_op:
    if item != "gps_points":
        print(f'{item} : {gpx_etl_op[item]}')

print('the end')
