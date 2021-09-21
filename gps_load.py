from jinja2 import FileSystemLoader, Environment

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
