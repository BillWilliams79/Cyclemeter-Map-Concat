import re, datetime

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
   
