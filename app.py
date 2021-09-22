from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect
import gps_transform, gps_extract, gps_load

app = Flask(__name__)

gpx_etl_op = dict()
gps_points = list()
gpx_etl_op["gps_points"] = gps_points
#
# initilize counters to zero
#
gpx_etl_op["imported_points"] = 0
gpx_etl_op["delta_points_stripped"] = 0
gpx_etl_op["current_points"] = 0


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/transferload", methods=["POST"])
def transferload():
    if request.method == 'POST':
        file_name = request.form.get("fname")
        min_delta = request.form.get("mdist")
        gpx_etl_op["extract_file_name"] = file_name
        gpx_etl_op["gps_min_delta"] = min_delta
        gpx_etl_op["gps_precision_reduction"] = 2
        gps_extract.gpx_file_extract(gpx_etl_op)
        return render_template('transferload.html', etl_op=gpx_etl_op)
    else:
        redirect("/")    
if __name__ == "__main__":
    app.run(debug=True)