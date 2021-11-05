from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
import gps_transform, gps_extract, gps_load, gps_utils
import pandas as pd
import sys

app = Flask(__name__)
etlop_df = pd.DataFrame()
run_df = pd.DataFrame()
etlop_df = gps_utils.init_etlop_df()
gps_utils.init_blue_descriptors(etlop_df)

@app.route("/")
def index():
    return render_template('gps_extract.html')


@app.route("/gps_transform", methods=["POST"])
def gps_transform_web():
    
    if request.method == 'POST':
        #
        # parse user input values using POST method
        #
        #etlop_df.at[0,"extract_source_type"] = file_name
        #etlop_df.at[0,"extract_file_name"] = 'Meter.db'
        etlop_df.at[0,"gps_min_delta"]  = int(request.form.get("gps_min_delta"))
        etlop_df.at[0,"gps_coord_precision"] = int(request.form.get("gps_coord_precision"))
        etlop_df.at[0,"load_file_type"] = request.form.get("load_file_type")
        etlop_df.at[0,"load_file_name"] = request.form.get("load_file_name")
        etlop_df.at[0,"gpx_name_string"] = request.form.get("gpx_name_string")
        #
        # alternate hard coded values. Should be either user input or hard coded.
        #
        etlop_df.at[0,"extract_source_type"] = 'cm'
        etlop_df.at[0,"extract_file_name"] = 'Meter.db'
        #etlop_df.at[0,"gps_min_delta"] = 5
        #etlop_df.at[0,"gps_coord_precision"] = '5'
        #etlop_df.at[0,"load_file_type"] = 'cm'
        #etlop_df.at[0,"load_file_name"] = 'tester'
        #etlop_df.at[0,"gpx_name_string"] = 'Bill and Tim Cycle the SF Bay Trail'
        
        # Debug Print to stderr
        #with pd.option_context("display.max_rows", 50, "display.max_columns", 20, "display.min_rows", 50):
        #    print('printing etlop_df prior to extract/transform')
        #    print(etlop_df, file=sys.stderr)
        #
        # extract and optimize
        #
        gps_extract.cm_sqlite3_extract(etlop_df)
        gps_transform.distance_optimizer(etlop_df)
        gps_transform.cm_data_format(etlop_df)        
        gps_transform.precision_optimizer(etlop_df)
        run_df = etlop_df.at[0,'run_df']
     
        percent_reduction = round(100 * run_df['stripped_points'].sum() / run_df['extracted_points'].sum(), 1)
        #
        # render and continue
        #
        return render_template('gps_transform.html', etlop_df=etlop_df, run_df = run_df, pr = percent_reduction)
    else:       
        redirect("/")    


@app.route("/gps_load", methods=["POST"])
def gps_load_web():
    if request.method == 'POST':
        #
        # GPS Transform
        #
        gps_load.kml_file_load(etlop_df)
        return render_template('gps_load.html', etlop_df=etlop_df)
    else:
        redirect("/")

@app.route("/gps_complete", methods=["POST"])
def gps_complete_web():
    if request.method == 'POST':
        #
        # GPS Transform
        #
        gps_load.gpx_file_load(etlop_df)
        return render_template('gps_complete.html', etlop_df=etlop_df)
    else:
        redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

