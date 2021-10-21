#
# imports
#
import gps_transform, gps_extract, gps_load
import pandas as pd
import datetime, time

#
# Data structures
#
def init_etlop_df():
    #
    # set column indexes and initial values for a gps ETL operation.
    #'', 'delta_points_stripped', '', 'gps_track_name', 'track_date_time',
    etlop_data_types = ['extract_source_type', 'extract_file_name', 'gps_coord_precision', 'gps_min_delta',  
                         'run_df', 'gps_df_list', 'gpx_name_string', 'gpx_date_string']
    etlop_init_stat = [[ '', '', int(), int(),
                         pd.DataFrame(), list(), '', datetime.datetime.now() ] ]
    return pd.DataFrame(etlop_init_stat, columns = etlop_data_types)

#
# initialize ETL operations dataframe
#
etlop_df = init_etlop_df()

# debugprint
#with pd.option_context("display.max_rows", 10, "display.max_columns", 15, "display.min_rows", 10):
#   print('\nPrint etlo_op dataframe initial creation.')
#   print(etlop_df)

#
# User Input: import type, source name, GPS min delta, coordinate precision
#
etlop_df.at[0,"extract_source_type"] = input('\nEnter GPS ETL source format (cm or gpx): ')
etlop_df.at[0,"extract_file_name"] = input('\nEnter GPS ETL source file name : ')
etlop_df.at[0,"gps_min_delta"] = int(input('Enter minimum distance between GPS points in meters : '))
etlop_df.at[0,"gps_coord_precision"] = int(input('Enter GPS coordinate precision (2-7) : '))

#manually construct the load file name.
etlop_df.at[0,"load_file_name"] = '{} {}m delta'.format(etlop_df.at[0,"extract_source_type"], etlop_df.at[0,"gps_min_delta"])

#manually set the gpx overall name string
etlop_df.at[0,"gpx_name_string"] = 'Bill and Tim Adventures'

#debug print
#with pd.option_context("display.max_rows", 10, "display.max_columns", 15, "display.min_rows", 10):
#    print("\nDisplay etlop_df after user input and prior to extract.")
#    print(etlop_df)

#
# GPS Extract
#
if etlop_df.at[0,"extract_source_type"] == 'gpx':
  #todo
  #gps_extract.gpx_file_extract(etlop_df)
  pass

else:
    #working
    gps_extract.cm_sqlite3_extract(etlop_df)

#debug print
#with pd.option_context("display.max_rows", 10, "display.max_columns", 20, "display.min_rows", 10):
#    print("\nDisplay run_df after extract.")
#    print(etlop_df.at[0,'run_df'])
#    print("\nPrint gps points list")
#    print(etlop_df.at[0, 'gps_points'])

#
# CLI screen prints post extraction
#
print('\n\nGPS track name\t\t\t: {}'.format(etlop_df.at[0,"gpx_name_string"]))
print(etlop_df.at[0,"gpx_date_string"].strftime('GPS track date\t\t\t: %A %B %d, %Y @ %I:%M%p'))
#print('GPS points extracted\t\t: {} (file: {})'.format(etlop_df.at[0,'imported_points'], etlop_df.at[0,'extract_file_name']))

#
# GPS Transform
#todo
#gps_transform.precision_optimizer(gpx_etl_op)
gps_transform.cm_data_format(etlop_df)
gps_transform.distance_optimizer(etlop_df)


#with pd.option_context("display.max_rows", 10, "display.max_columns", 20, "display.min_rows", 10):
#    print("\nDisplay run_df after Transform.")
#    print(etlop_df.at[0,'run_df'])
#    print("\nPrint gps points list")
#    print(etlop_df.at[0, 'gps_points'])



#print('GPS points stripped @ {}m\t: {}'.format(etlop_df.at[0,'gps_min_delta'], etlop_df.at[0,'delta_points_stripped']))  
#print('GPS points after distance strip\t: {}'.format(etlop_df.at[0,"current_points"]))
#percent_reduction = round(100 * etlop_df.at[0,'delta_points_stripped'] / etlop_df.at[0,'imported_points'], 1)
#print('\nGPS points reduced %g percent' % (percent_reduction))  

#
# GPS load
#todo
gps_load.gpx_file_load_trk(etlop_df)

#
# DEBUG: Print the items in the main dictionary for debug purposes
# Skipping the list of points of course
#
#print(' ')
#for item in gpx_etl_op:
#    if item != "gps_points":
#        print(f'{item} : {gpx_etl_op[item]}')

print('\nThe end')
