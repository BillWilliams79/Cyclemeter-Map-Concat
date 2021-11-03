from geopy import distance
import datetime, time
import pandas as pd
import decimal as decimal

Decimal = decimal.Decimal


def precision_optimizer(etlop_df):
    #
    # precision optimizer - drop 2 digits from lat, lon, and ele.
    #
    precision = etlop_df.at[0, "gps_coord_precision"]

    if precision == 0:
        #
        # 0 = no work to be done
        #
        return
    else:
        new_precision = Decimal.shift(Decimal(1), int(precision))
        new_precision = 1 / new_precision
        #print(decimal.Context.prec)
        print(new_precision)

    points_df_list = etlop_df.at[0, "gps_df_list"]

    for index, points_df in enumerate(points_df_list):
        points_df['latitude'] = points_df['latitude'].apply(lambda latitude: float(Decimal.from_float(latitude).quantize(Decimal(new_precision))))
        points_df['longitude'] = points_df['longitude'].apply(lambda longitude: float(Decimal.from_float(longitude).quantize(Decimal(new_precision))))
 #       points_df['elevation'] = points_df['elevation'].apply(lambda elevation: float(Decimal.from_float(elevation).quantize(Decimal(precision))))

    # debug print
    with pd.option_context("display.max_rows", 50, "display.max_columns", 15, "display.min_rows", 50):
        print(points_df)


def df_itertuple_generator(df):
    for gps_point in df.itertuples():
        yield gps_point


def distance_optimizer(etlop_df):
    
    run_df = etlop_df.at[0,"run_df"]
    points_df_list = etlop_df.at[0, "gps_df_list"]

    #
    # for every row in run_df there is a points dataframe in points_df_list, with the same index.
    # We will iterate over the points_df_list, performing the minimum GPS distance
    # calculations and use the index from that iteration to record outcome stats
    # in run_df
    #
    # list iterator to retrieve points_df (and index)
    ## TODO: change the index to run_index to mirror gps_index.
    for index, points_df in enumerate(points_df_list):

        # created a generator to have better control over the iteration across
        # the dataframe using itertuple
        df_iter = df_itertuple_generator(points_df)
        points_drop_list = list()
        run_df.at[index,"current_points"] = 0

        #print(f'Optimize ride # {index}\n')
        #
        # loop assumese current point is set and loop sets compare point next
        # just instatiated the generator and therefore the first element is current
        gps_point = next(df_iter)
        current_point = (gps_point.latitude, gps_point.longitude)
        
        # iterate over the rows of the points database
        # itertuple generator returns the rows as a namedTuple.
        # TODO: gps_point should be compare_gps_point. embrace the beauty
        for gps_index, gps_point in enumerate(df_iter):
            #
            # process GPS points one dataframe row at a time.
            #
            # use a df.itertuple generator to allow for looping but also loop advance
            # as points are discarded for being too close together

            compare_point = (gps_point.latitude, gps_point.longitude)
            mydistance = distance.distance(current_point, compare_point)
            #
            # If the distance between current and next points is less than the minimum delta,
            # add its index to drop list and record activty. 
            #
            if round(mydistance.m,1) < etlop_df.at[0,"gps_min_delta"]:
                #
                # DROP POINT - LESS THAN MIN
                # drop: append compare_point (gps_index?) to drop list. Record delta_points_stripiped +1.
                #print('drop: {} {} {}'.format(gps_point.Index, mydistance.m, run_df.at[index, "stripped_points"]))
                points_drop_list.append(gps_point.Index)
                run_df.at[index, "stripped_points"] += 1
                continue
            else:
                #
                # ACCEPT POINT - MORE THAN MIN
                # The compare_point is more than the minimum. Therefore compare points becomes
                # the new head (aka current point) and we iterate through the loop again.
                current_point = compare_point
                run_df.at[index,"current_points"] += 1
                continue
        #
        # one complete set of gps points has been processed. Must execute the drop command
        # on the drop list and renumber the index.
        #
        points_df.drop(points_drop_list, axis = 0, inplace=True)
        points_df.reset_index(inplace=True, drop=True)
        #print('MIN DIST Complete extracted:current:dropped {}:{}:{}'.format(run_df.at[index,"extracted_points"],run_df.at[index,"current_points"],run_df.at[index, "stripped_points"]))
        #print(points_df.head(6))            

def startTime_tz_adjust(startTime):
            #
            # just using the most brutal month granular adjustment for DST
            # TODO: actually implement correct DST adjustment
            #
            dt = datetime.datetime.fromisoformat(startTime)

            if dt.month in ('1', '2', '3', '11', '12'):
                tzadjust = datetime.timedelta(hours = 8)
            else:
                tzadjust = datetime.timedelta(hours = 7)
            
            return dt - tzadjust

def cm_data_format(etlop_df):
    
    run_df = etlop_df.at[0,'run_df']
    #
    # Cyclemeter Transform
    #
    dt = datetime.datetime
    dt_time = datetime.time

    for run in run_df.itertuples():
        run_df.at[run.Index,'average_speed'] = Decimal(run_df.at[run.Index,'distance'] / run_df.at[run.Index,'runTime'] * 2.237).quantize(Decimal('0.01'))

    # limit stopped time to 24 hours
    run_df['stoppedTime'] = run_df['stoppedTime'].apply(lambda stoppedTime: min(stoppedTime, 24*60*60-1))

    # xlat startTime from isoformat to gis format and two formats for display in kml balloons
    # note: creating and storing two pre-formatted time strings becuase Jinja2 doesn't elegently handle
    #       strftime formatting in situ.
    run_df['startTime'] = run_df['startTime'].apply(lambda startTime: startTime_tz_adjust(startTime))
    run_df['formatted_startTime'] = run_df['startTime'].apply(lambda startTime: startTime.strftime('%A %b %d, %Y @ %I:%M%p'))
    run_df['title_formatted_startTime'] = run_df['startTime'].apply(lambda startTime: startTime.strftime('%Y-%b-%d'))

    # convert cyclemeter's time format of seconds to H:M:S using datetime.
    run_df['runTime'] = run_df['runTime'].apply(lambda runTime: time.strftime('%H:%M:%S', time.gmtime(runTime)))
    run_df['stoppedTime'] = run_df['stoppedTime'].apply(lambda runTime: time.strftime('%H:%M:%S', time.gmtime(runTime)))

    # convert from meters to miles (distance/1609).
    # Use decimal "quantize" to strip to exact precision
    run_df['distance'] = run_df['distance'].apply(lambda distance: float(Decimal.from_float(distance / 1609).quantize(Decimal('0.1'))))

    # convert from meters to feet
    # Use decimal "quantize" to strip to exact precision
    # ascent/descent = meters to feet; maxSpeed = m/s to miles/hour
    run_df['ascent'] = run_df['ascent'].apply(lambda ascent: int(ascent * 3.281))
    run_df['descent'] = run_df['descent'].apply(lambda descent: int(descent * 3.281))
    run_df['maxSpeed'] = run_df['maxSpeed'].apply(lambda maxSpeed: float(Decimal.from_float(maxSpeed * 2.237).quantize(Decimal('0.1'))))

    # set precision
    run_df['calories'] = run_df['calories'].apply(lambda calories: int(calories))

    # debug print
    with pd.option_context("display.max_rows", 50, "display.max_columns", 15, "display.min_rows", 50):
        print(run_df)

