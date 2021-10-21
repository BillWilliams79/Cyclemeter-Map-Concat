from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
import gps_transform, gps_extract, gps_load

app = Flask(__name__)

gpx_etl_op = dict()
gps_points = list()
gpx_etl_op["gps_points"] = gps_points

def init_etl_op(etl_op):
    #
    # initilize structure to zero.
    # demonstrates how this should become a class, no?
    #
    gpx_etl_op["imported_points"] = 0
    gpx_etl_op["delta_points_stripped"] = 0
    gpx_etl_op["current_points"] = 0
    gpx_etl_op["extract_file_name"] =''
    gpx_etl_op["load_file_name"] = ''
    gpx_etl_op['gpx_track_name'] = ''
    gpx_etl_op["gps_points"].clear()

def init_etlop_df(df):
    etlop_data_types = ['imported_points', "delta_points_stripped", "current_points", "extract_file_name"
                        'load_file_name', 'gpx_track_name', 'gps_points']
    df = pd.DataFrame(columns = etlop_data_types)

@app.route("/")
def index():
    init_etl_op(gpx_etl_op)
    return render_template('gps_extract.html')


@app.route("/gps_transform", methods=["POST"])
def gps_transform_web():
    if request.method == 'POST':
        #
        # parse user input values using POST method
        #
        file_name = request.form.get("file_name")
        min_delta = int(request.form.get("min_dist"))
        precision_reduction = int(request.form.get("precision_optimizer"))
        gpx_etl_op["extract_file_name"] = file_name
        gpx_etl_op["gps_min_delta"] = min_delta
        gpx_etl_op["gps_precision_reduction"] = precision_reduction
        gpx_etl_op["load_file_name"] = 'Strava GPX {gps_min_delta}m {gps_precision_reduction}pr delta'.format(**gpx_etl_op)
        #
        # extract and optimize
        #
        gps_extract.gpx_file_extract(gpx_etl_op)
        gps_transform.distance_optimizer(gpx_etl_op)
        gps_transform.precision_optimizer(gpx_etl_op)
        gps_date = gpx_etl_op["track_date_time"].strftime('%A %B %d, %Y @ %I:%M%p')
        percent_reduction = round(100 * (gpx_etl_op["delta_points_stripped"] / gpx_etl_op["imported_points"]), 1)
        #
        # render and continue
        #
        return render_template('gps_transform.html', etl_op=gpx_etl_op, gps_date = gps_date, pr = percent_reduction)
    else:       
        redirect("/")    


@app.route("/gps_load", methods=["POST"])
def gps_load_web():
    if request.method == 'POST':
        #
        # GPS Transform
        #
        gps_load.gpx_file_load(gpx_etl_op)
        return render_template('gps_load.html', etl_op=gpx_etl_op)
    else:
        redirect("/")

@app.route("/gps_complete", methods=["POST"])
def gps_complete_web():
    if request.method == 'POST':
        #
        # GPS Transform
        #
        gps_load.gpx_file_load(gpx_etl_op)
        return render_template('gps_complete.html', etl_op=gpx_etl_op)
    else:
        redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

