from jinja2 import FileSystemLoader, Environment
import pandas as pd
import datetime, time

def gpx_file_load(etl_op):
    #
    # Now store gps points in strava gpx file using Jinja2
    #
    file_loader = FileSystemLoader('Templates')
    Env = Environment(loader=file_loader, trim_blocks=True)

    template = Env.get_template('child.txt')

    handle = open(etl_op["load_file_name"].lower() + ".gpx", "w")
    handle.write(template.render(ride_title = etl_op["load_file_name"], gps_list = etl_op["gps_points"]))
    handle.close()

def kml_file_load(etl_op):
    #
    # Now store gps points in a kml file using Jinja2
    #
    file_loader = FileSystemLoader('Templates')
    Env = Environment(loader=file_loader, trim_blocks=True)

    kml_template = Env.get_template('kml_file_template.txt')

    handle = open(etl_op["load_file_name"].lower() + ".kml", "w")
    handle.write(kml_template.render(ride_title = etl_op["load_file_name"], gps_list = etl_op["gps_points"]))
    handle.close()

def gpx_file_load_trk(etlop_df):
    
    df = etlop_df.at[0,'run_df']
    dt = datetime.datetime
#    dt_time = datetime.time

    points_list = etlop_df.at[0,'gps_df_list']
    #
    # Now store gps points in strava gpx file using Jinja2
    #
    file_loader = FileSystemLoader('Templates')
    Env = Environment(loader=file_loader, trim_blocks=True)

    gpx_template = Env.get_template('gpx_template.txt')
    trk_template = Env.get_template('trk_template.txt')

    handle = open("BillandTimAdventures.gpx", "w")

    #
    # Use itertuples to iterate each row in the run datatframe.
    # itertuples returns the run as a namedtuple including the Index.
    # Dot notation allows access to memebers of the namedtuple
    #
    trk_accumulator = str('')

    for cm_run in df.itertuples():
        #
        # render a track template and concatanate with the accumulator
        #
        trk_accumulator += trk_template.render(ride_title = cm_run.notes, gpx_track_date = cm_run.startTime, df = points_list[cm_run.Index])

        #
        # like it or not we have to cap the GPX file size below 5MB
        #
        if len(trk_accumulator) > 4900000:
            print('\nReached max GPX size limit, processing stop at {} runs'.format(cm_run.Index))
            break;
        else:
            #
            # newline required between TRK's but not after the last one.
            #
            trk_accumulator += '\n'

    #
    # second render stage, take accumulator and the date to make the file
    #
    print('TRK total size:\t{}'.format(len(trk_accumulator)))
    print('TRK total runs:\t{}'.format(cm_run.Index))

    gpx_render = gpx_template.render(trk_renders = trk_accumulator, gpx_track_date = dt.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ'))

    handle.write(gpx_render)
    handle.close()
