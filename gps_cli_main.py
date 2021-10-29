#
# imports
#
from os import X_OK
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
    etlop_column_names = ['extract_source_type', 'extract_file_name', 'gps_coord_precision', 'gps_min_delta',  
                         'run_df', 'gps_df_list',
                         'gpx_name_string', 'gpx_date_string', 'icon_descriptor_df', 'line_descriptor_df',
                         'load_file_type', 'load_file_name']
    
    etlop_initial_values = [[ str(), str(), int(), int(),
                         pd.DataFrame(), list(),
                         str(), datetime.datetime.now(), pd.DataFrame(), pd.DataFrame(),
                         str(), str() ]]

    return pd.DataFrame(etlop_initial_values, columns = etlop_column_names)


def init_rainbow_descriptors():
  #
  # brutal hard coding of color values
  #
  icon_column_list = ['icon_type', 'icon_color', 'icon_color_id']
  icon_descriptor_list = [[ '1522', 'ff5b18c2', 'C2185B' ], # red
                          [ '1522', 'ff007cf5', 'F57C00' ], # orange
                          [ '1522', 'ff25a8f9', 'F9A825' ], # dark yellow
                          [ '1522', 'ff42b37c', '7CB342' ], # lite green
                          [ '1522', 'ff387109', '097138' ], # dark green
                          [ '1522', 'ffa79700', '0097A7' ], # lite blue
                          [ '1522', 'ffab4939', '3949AB' ], # dark blue
                          [ '1522', 'ffb0279c', '9C27B0' ]] # violet

  line_column_list = ['line_color', 'line_color_id']
  line_descriptor_list = [['ff5b18c2', 'C2185B' ], # red
                          ['ff007cf5', 'F57C00' ], # orange
                          ['ff25a8f9', 'F9A825' ], # dark yellow
                          ['ff42b37c', '7CB342' ], # lite green
                          ['ff387109', '097138' ], # dark green
                          ['ffa79700', '0097A7' ], # lite blue
                          ['ffab4939', '3949AB' ], # dark blue
                          ['ffb0279c', '9C27B0' ]] # violet

  etlop_df.at[0,'icon_descriptor_df'] = pd.DataFrame(icon_descriptor_list, columns = icon_column_list)
  etlop_df.at[0,'line_descriptor_df'] = pd.DataFrame(line_descriptor_list, columns = line_column_list)  

def init_blue_descriptors():
  #
  # brutal hard coding of color values
  #
  icon_column_list = ['icon_type', 'icon_color', 'icon_color_id']
  icon_descriptor_list = [[ '1522', 'ff4c2503', '03254c' ], # dark blue
                          [ '1522', 'ffb16711', '1167b1' ], # 
                          [ '1522', 'ffcd7b18', '187bcd' ], #  
                          [ '1522', 'fff49d2a', '2a9df4' ], #  
                          [ '1522', 'ff807868', '687880' ]] # very lite blue

  line_column_list = ['line_color', 'line_color_id']
  line_descriptor_list = [['ff4c2503', '03254c' ], # dark blue
                          ['ffb16711', '1167b1' ], # 
                          ['ffcd7b18', '187bcd' ], #  
                          ['fff49d2a', '2a9df4' ], #  
                          ['ff807868', '687880' ]] # very lite blue


  etlop_df.at[0,'icon_descriptor_df'] = pd.DataFrame(icon_descriptor_list, columns = icon_column_list)
  etlop_df.at[0,'line_descriptor_df'] = pd.DataFrame(line_descriptor_list, columns = line_column_list)  
#
# initialize ETL operations dataframe and gis descriptors
#
etlop_df = init_etlop_df()
init_blue_descriptors()

# debugprint
#with pd.option_context("display.max_rows", 10, "display.max_columns", 15, "display.min_rows", 10):
#  print('\nPrint etlo_op dataframe initial creation.')
#  print(etlop_df.at[0,'icon_descriptor_df'])
#  print(etlop_df.at[0,'line_descriptor_df'])
#
# User Input: import type, source name, GPS min delta, coordinate precision
#
#etlop_df.at[0,"extract_source_type"] = input('\nEnter GPS ETL source format (cm or gpx): ')
#etlop_df.at[0,"extract_file_name"] = input('\nEnter GPS ETL source file name : ')
#etlop_df.at[0,"gps_min_delta"] = int(input('Enter minimum distance between GPS points in meters : '))
#etlop_df.at[0,"gps_coord_precision"] = int(input('Enter GPS coordinate precision (2-7) : '))
etlop_df.at[0,"extract_source_type"] = 'cm'
etlop_df.at[0,"extract_file_name"] = 'Meter.db'
etlop_df.at[0,"gps_min_delta"] = 25
etlop_df.at[0,"gps_coord_precision"] = 5

etlop_df.at[0,"load_file_type"] = input('Enter Save File Type: ')
etlop_df.at[0,"load_file_name"] = input('Enter Save File Name: ')


#manually construct the load file name.
#etlop_df.at[0,"load_file_name"] = '{} {}m delta'.format(etlop_df.at[0,"extract_source_type"], etlop_df.at[0,"gps_min_delta"])

#manually set the gpx overall name string
etlop_df.at[0,"gpx_name_string"] = 'Bill and Tim Cycle the SF Bay Trail'

#
# GPS Extract
#
print('\nInitiate EXTRACT...')
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
print('\nInitiate TRANSFORM...')
#gps_transform.precision_optimizer(gpx_etl_op)
gps_transform.cm_data_format(etlop_df)
gps_transform.distance_optimizer(etlop_df)


#with pd.option_context("display.max_rows", 10, "display.max_columns", 20, "display.min_rows", 10):
#    print("\nDisplay run_df after Transform.")
#    print(etlop_df.at[0,'run_df'])
#    print("\nPrint gps points list")
#    print(etlop_df.at[0, 'gps_points'])


#
# TODO: fix prints for multi-file support
#
#print('GPS points stripped @ {}m\t: {}'.format(etlop_df.at[0,'gps_min_delta'], etlop_df.at[0,'delta_points_stripped']))  
#print('GPS points after distance strip\t: {}'.format(etlop_df.at[0,"current_points"]))
#percent_reduction = round(100 * etlop_df.at[0,'delta_points_stripped'] / etlop_df.at[0,'imported_points'], 1)
#print('\nGPS points reduced %g percent' % (percent_reduction))  

#
# GPS load
#
print('\nInitiate LOAD...')
if etlop_df.at[0,"load_file_type"] == 'gpx':
  gps_load.gpx_file_load_trk(etlop_df)

elif etlop_df.at[0,"load_file_type"] == 'kml':
  gps_load.kml_file_load(etlop_df)

print('\nThe end')
