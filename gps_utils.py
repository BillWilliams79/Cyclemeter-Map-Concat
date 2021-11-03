import pandas as pd
import datetime

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
    
    etlop_initial_values = [[ str(), str(), str(), int(),
                         pd.DataFrame(), list(),
                         str(), datetime.datetime.now(), pd.DataFrame(), pd.DataFrame(),
                         str(), str() ]]

    return pd.DataFrame(etlop_initial_values, columns = etlop_column_names)


def init_rainbow_descriptors(etlop_df):
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

def init_blue_descriptors(etlop_df):
  #
  # brutal hard coding of color values
  #
  icon_column_list = ['icon_type', 'icon_color', 'icon_color_id']
  icon_descriptor_list = [[ '1522', 'ff4c2503', '03254c' ], # dark blue - Bike icon
                          [ '1522', 'ffb16711', '1167b1' ], # 
                          [ '1522', 'ffcd7b18', '187bcd' ], #  
                          [ '1522', 'fff49d2a', '2a9df4' ], #  
                          [ '1522', 'ffffbfa6', 'a6bfff' ], # very lite blue
                          [ '1596', 'ff4c2503', '03254c' ], # dark blue - Hike icon
                          [ '1596', 'ffb16711', '1167b1' ], # 
                          [ '1596', 'ffcd7b18', '187bcd' ], #  
                          [ '1596', 'fff49d2a', '2a9df4' ], #  
                          [ '1596', 'ffffbfa6', 'a6bfff' ]] # very lite blue

  line_column_list = ['line_color', 'line_color_id']
  line_descriptor_list = [['ff4c2503', '03254c' ], # dark blue
                          ['ffb16711', '1167b1' ], # 
                          ['ffcd7b18', '187bcd' ], #  
                          ['fff49d2a', '2a9df4' ], #  
                          ['ffffbfa6', 'a6bfff' ]] # very lite blue


  etlop_df.at[0,'icon_descriptor_df'] = pd.DataFrame(icon_descriptor_list, columns = icon_column_list)
  etlop_df.at[0,'line_descriptor_df'] = pd.DataFrame(line_descriptor_list, columns = line_column_list)  