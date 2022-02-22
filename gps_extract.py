import re, datetime
import pandas as pd
import sqlite3
import itertools
import sys

def gpx_file_extract(etl_op):

    fileHandle = open(etl_op["extract_file_name"])
    points_list = etl_op["gps_points"]

    latCount = 0
    lonCount = 0
    eleCount = 0
    gpsTimeCount = 0

    #
    # commence parsing the metadata section first before parsing the GPS points
    #
    for line in fileHandle:
        dt = datetime.datetime
        date = re.findall('<time>([0-9:T\-]+)', line)
        if len(date) > 0:
            etl_op["track_date_time"] = dt.fromisoformat(date[0])
            #
            # just using the most brutal month granular adjustment for DST
            # TODO: actually implement correct DST adjustment
            #
            if dt.month in ('1', '2', '3', '11', '12'):
                tzadjust = datetime.timedelta(hours = 8)
            else:
                tzadjust = datetime.timedelta(hours = 7)
            etl_op["track_date_time"] = etl_op["track_date_time"] - tzadjust
            break

        if len(re.findall('</metadata>', line)) > 0:
            # metadata end tag, stop processing.
            break
        else:
            continue

    #
    # process file line by line looking for track points and eleveation data.
    # these three values consume two lines in gpx files with elevation
    # on the secone line. So lat/lon are collected first and then
    # the data is stuffed into a list of dictionaries. 
    # Also the name of the track is included in the points list. 
    #
    for line in fileHandle:
        #
        # regular expression method of finding values
        #
        name = re.findall('<name>([a-z A-Z.,!?:;@&]+)', line)
        if name != []:
            etl_op["gps_track_name"] = name[0]

        lat = re.findall('lat="([0-9.-]+)', line)
        if lat != []:
            points_list.append(dict({'latitude' : lat[0]}))
            latCount += 1

        lon = re.findall('lon="([0-9.-]+)', line)
        if lon != []:
            points_list[len(points_list) - 1]['longitude'] = lon[0]
            lonCount += 1

        ele = re.findall('<ele>([0-9.-]+)', line)
        if ele != []:
            points_list[len(points_list) - 1]['elevation'] = ele[0]
            eleCount += 1

        gpsTime = re.findall('<time>([0-9.\-:T]+)', line)
        if gpsTime != []:
            points_list[len(points_list) - 1]['gpstime'] = gpsTime[0]
            gpsTimeCount += 1
        
            #
            # DEBUG: breaks points extraction processing after 5 gps points
            #
            #count = count + 1
            #if count == 5:
            #    print(points_list)
            #    break        

    etl_op["imported_points"] = len(points_list)


#
#
#
def gpx_file_extract_to_df(etl_op):

    fileHandle = open(etl_op["extract_file_name"])
    points_list = etl_op["gps_points"]

    latCount = 0
    lonCount = 0
    eleCount = 0
    gpsTimeCount = 0

    #
    # commence parsing the metadata section first before parsing the GPS points
    #
    for line in fileHandle:
        dt = datetime.datetime
        date = re.findall('<time>([0-9:T\-]+)', line)
        if len(date) > 0:
            etl_op["track_date_time"] = dt.fromisoformat(date[0])
            #
            # just using the most brutal month granular adjustment for DST
            # TODO: actually implement correct DST adjustment
            #
            if dt.month in ('1', '2', '3', '11', '12'):
                tzadjust = datetime.timedelta(hours = 8)
            else:
                tzadjust = datetime.timedelta(hours = 7)
            etl_op["track_date_time"] = etl_op["track_date_time"] - tzadjust
            break

        if len(re.findall('</metadata>', line)) > 0:
            # metadata end tag, stop processing.
            break
        else:
            continue

    #
    # process file line by line looking for track points and eleveation data.
    # these three values consume two lines in gpx files with elevation
    # on the secone line. So lat/lon are collected first and then
    # the data is stuffed into a list of dictionaries. 
    # Also the name of the track is included in the points list. 
    #
    for line in fileHandle:
        #
        # regular expression method of finding values
        #
        name = re.findall('<name>([a-z A-Z.,!?:;@&]+)', line)
        if name != []:
            etl_op["gps_track_name"] = name[0]

        lat = re.findall('lat="([0-9.-]+)', line)
        if lat != []:
            points_list.append(dict({'latitude' : lat[0]}))
            latCount += 1

        lon = re.findall('lon="([0-9.-]+)', line)
        if lon != []:
            points_list[len(points_list) - 1]['longitude'] = lon[0]
            lonCount += 1

        ele = re.findall('<ele>([0-9.-]+)', line)
        if ele != []:
            points_list[len(points_list) - 1]['elevation'] = ele[0]
            eleCount += 1

        gpsTime = re.findall('<time>([0-9.\-:T]+)', line)
        if gpsTime != []:
            points_list[len(points_list) - 1]['gpstime'] = gpsTime[0]
            gpsTimeCount += 1
        
            #
            # DEBUG: breaks points extraction processing after 5 gps points
            #
            #count = count + 1
            #if count == 5:
            #    print(points_list)
            #    break        

    etl_op["imported_points"] = len(points_list)


def cm_sqlite3_extract(etlop_df):

    #
    # connect to cyclemeter's sqlite3 database.
    # database acuired from my phone (Bill) Sep '21
    #
    con = sqlite3.connect(etlop_df.at[0,"extract_file_name"])

    # from the SQLite connection, create a curosr
    cur = con.cursor()

    #
    # EXTRACT: Cyclemeter run extract while pruning unused columns
    #
    #
    # SQL command that extracts and cleans cyclemeter runs.
    # Does a join with the route table to retrieve the cycelmenet route name 
    cm_extract_sql = """
                        SELECT
                            run.runID,
                            run.routeID,
                            activityID,
                            route.name,
                            startTime,
                            runTime,
                            stoppedTime,
                            distance,
                            ascent,
                            descent,
                            calories,
                            maxSpeed,
                            notes
                        FROM
                            run
                        JOIN
                            route USING(routeID)
                        WHERE
                            run.routeID=56 OR run.routeID=10
                        ORDER BY
                            run.startTime ASC
                    """

    notes_extract_sql = """
                        SELECT
                            run.runID,
                            run.routeID,
                            activityID,
                            route.name,
                            startTime,
                            runTime,
                            stoppedTime,
                            distance,
                            ascent,
                            descent,
                            calories,
                            maxSpeed,
                            notes
                        FROM
                            run
                        JOIN
                            route USING(routeID)
                        WHERE
                            run.notes LIKE '%jim %'
                    """

    #
    # extract cyclemeter run into a dataframe where each row is a separate run
    #
    print('priting cm extract sql')
    print(cm_extract_sql);
    etlop_df.at[0,"run_df"] = pd.read_sql_query(cm_extract_sql, con)
    # use temp option_context to alter display details of a pandas dataframe
    #with pd.option_context("display.max_rows", 20, "display.max_columns", 15, "display.min_rows", 20):
    #    print(etlop_df.at[0,"run_df"] )

    # Post SQL extractioin of run data, add stats column to dataframe
    run_df = etlop_df.at[0,"run_df"]
    run_df['extracted_points'] = 0
    run_df['current_points'] = 0
    run_df['stripped_points'] = 0
    run_df['line_color_id'] = ''
    run_df['line_icon_id'] = int()
    run_df['activity_name'] = ''
    run_df['average_speed'] = float()

    # per ride line color, line icon type and activity name assignment
    # note: frustratingly cannot find the activityID->activityName mapping in the sql database.
    #       schema refers to an activityNameStr under activity but has no index, string or mapping.
    #       only alternative is to hand code values.
    color_cycle = itertools.cycle(etlop_df.at[0,"line_descriptor_df"]['line_color_id'].tolist())
    for run in run_df.itertuples():
        run_df.at[run.Index,'line_color_id'] = next(color_cycle)
        run_df.at[run.Index,'activity_name'] = 'Ride' if run_df.at[run.Index,'activityID'] == 4 else 'Hike'
        run_df.at[run.Index,'line_icon_id'] = 1522 if run_df.at[run.Index, 'activityID'] == 4 else 1596

    #
    # use list comprehension to iterate over the runIDs and build a list of dataframes with GPS points 
    #todo security
    etlop_df.at[0,"gps_df_list"] = [pd.read_sql_query('SELECT * FROM coordinate WHERE runID={}'.format(runID), con) for label, runID in etlop_df.at[0,"run_df"]['runID'].items()]

    # calculate the number of points extracted from each run, which is also the current_points
    for index, points_df in enumerate(etlop_df.at[0, "gps_df_list"]):
        num_rows, num_cols = points_df.shape
        run_df.at[index,"extracted_points"] = num_rows
        run_df.at[index,"current_points"] = num_rows
    
    #debugprint
    #with pd.option_context("display.max_rows", 50, "display.max_columns", 15, "display.min_rows", 50):
    #    print(run_df, file=sys.stderr)
