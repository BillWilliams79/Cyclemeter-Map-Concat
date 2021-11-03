#
# Python imports
#
import gps_transform, gps_extract, gps_load, gps_utils
import pandas as pd
import datetime, time
import os


#
# initialize ETL operations dataframe and gis descriptors
#
etlop_df = gps_utils.init_etlop_df()
gps_utils.init_blue_descriptors(etlop_df)


#
# User Input: import type, source name, GPS min delta, coordinate precision
#
#etlop_df.at[0,"extract_source_type"] = input('\nEnter GPS ETL source format (cm or gpx): ')
#etlop_df.at[0,"extract_file_name"] = input('\nEnter GPS ETL source file name : ')
etlop_df.at[0,"gps_min_delta"] = int(input('Enter minimum distance between GPS points in meters : '))
#etlop_df.at[0,"gps_coord_precision"] = int(input('Enter GPS coordinate precision (2-7) : '))
etlop_df.at[0,"load_file_type"] = input('Enter Save File Type (kml or gpx): ')
etlop_df.at[0,"load_file_name"] = input('Enter Save File Name: ')
#etlop_df.at[0,"gpx_name_string"] = input('Enter overall file name string')
#
# alternate hard coded values. Should be either user input or hard coded.
#
etlop_df.at[0,"extract_source_type"] = 'cm'
etlop_df.at[0,"extract_file_name"] = 'Meter.db'
#etlop_df.at[0,"gps_min_delta"] = 5
etlop_df.at[0,"gps_coord_precision"] = '5'
#etlop_df.at[0,"load_file_type"] = 'cm'
#etlop_df.at[0,"load_file_name"] = 'tester'
etlop_df.at[0,"gpx_name_string"] = 'Bill and Tim Cycle the SF Bay Trail'

#
# GPS Extract
#
print('\nInitiate EXTRACT...', end='')
if etlop_df.at[0,"extract_source_type"] == 'gpx':
  #todo
  #gps_extract.gpx_file_extract(etlop_df)
  pass
else:
    #working
    gps_extract.cm_sqlite3_extract(etlop_df)
print('completed.')

#debug print
#with pd.option_context("display.max_rows", 50, "display.max_columns", 20, "display.min_rows", 50):
#    print("\nDisplay run_df after extract.")
#    print(etlop_df.at[0,'run_df'])

#
# CLI screen prints post extraction
#
run_df = etlop_df.at[0,'run_df']
print('Cyclemeter activites extracted\t: {}'.format(run_df.shape[0]))


#
# GPS Transform
#
print('\nInitiate TRANSFORM...', end='')
gps_transform.precision_optimizer(etlop_df)
gps_transform.cm_data_format(etlop_df)
gps_transform.distance_optimizer(etlop_df)
print('completed.')

#with pd.option_context("display.max_rows", 50, "display.max_columns", 20, "display.min_rows", 50):
#    print("TRANSFORM complete. Display run_df\n")
#    print(etlop_df.at[0,'run_df'])

#
# Post TRANSFORM screen prints
#
print('Activity Total Distance\t\t: {} miles'.format(round(run_df['distance'].sum(),1)))
print('Total GPS points extracted\t: {:,}'.format(run_df['extracted_points'].sum()))
print('Total GPS points stripped @ {}m\t: {:,}'.format(etlop_df.at[0,'gps_min_delta'], run_df['stripped_points'].sum()))
print('Total GPS points remaining\t: {:,}'.format(run_df['current_points'].sum()))
percent_reduction = round(100 * run_df['stripped_points'].sum() / run_df['extracted_points'].sum(), 1)
print('GPS points reduced\t\t: {} %'.format(percent_reduction))  


#
# GPS load
#
print('\nInitiate LOAD...', end='')
if etlop_df.at[0,"load_file_type"] == 'gpx':
  gps_load.gpx_file_load_trk(etlop_df)

elif etlop_df.at[0,"load_file_type"] == 'kml':
  gps_load.kml_file_load(etlop_df)
print('completed.')

load_string = '{}.{}'.format(etlop_df.at[0,'load_file_name'],etlop_df.at[0,'load_file_type'])
print('Saved file {}, file size\t: {} MB'.format(load_string, round(os.path.getsize(load_string) / (1024*1024),2)))

print('\nThe end')
