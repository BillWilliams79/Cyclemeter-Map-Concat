import re

def gpx_file_extract(fileName, points_list):

    fileHandle = open(fileName)
    count = 0
    dataList = list()
    latCount = 0
    lonCount = 0
    eleCount = 0
    gpsTimeCount = 0

    #
    # commence parsing the metadata section first before parsing the GPS points
    #
    for line in fileHandle:

        if len(re.findall('</metadata>', line)) > 0:
            # metadata end tag, stop processing.
            break
        else:
            continue

    #
    # process file line by line looking for track points and eleveation data.
    # these three values consume two lines in gpx files with elevation
    # on the secone line. So lat/lon are collected first and then
    # the data is stuffed into a list of dictionaries
    #
    for line in fileHandle:
        #
        # regular expression method of finding values
        #
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
        
            #this debug code breaks the ingest points processing after 5 gps points
            #count = count + 1
            #if count == 5:
            #    print(points_list)
            #    break        

    imported_points = len(points_list)
    print('\nGPS points imported\t\t: %d' % imported_points)
