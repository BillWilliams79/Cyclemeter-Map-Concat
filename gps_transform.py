#
# precision optimizer - drop 2 digits from lat, lon, and ele.
#
def precision_optimizer(points_list, precision_reduction):
   for gps_point in points_list:
       gps_point['latitude'] = gps_point['latitude'][0:len(gps_point['latitude']) - precision_reduction]
       gps_point['longitude'] = gps_point['longitude'][0:len(gps_point['longitude']) - precision_reduction]
       gps_point['elevation'] = gps_point['elevation'][0:len(gps_point['elevation']) - precision_reduction]