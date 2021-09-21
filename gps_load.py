from jinja2 import FileSystemLoader, Environment

def gpx_file_load(points_list, etl_name):
    #
    # Now store gps points in strava gpx file using Jinja2
    #
    file_loader = FileSystemLoader('Templates')
    Env = Environment(loader=file_loader, trim_blocks=True)

    template = Env.get_template('child.txt')


    handle = open(etl_name.lower() + ".gpx", "w")
    handle.write(template.render(ride_title = etl_name, gps_list = points_list))
    handle.close()
