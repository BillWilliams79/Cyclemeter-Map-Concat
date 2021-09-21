from geopy import distance
#import pandas as pd

#
# precision optimizer - drop 2 digits from lat, lon, and ele.
#
def precision_optimizer(etl_op):

    precision_reduction = etl_op["gps_precision_reduction"]

    for point in etl_op["gps_points"]:
       point['latitude']  = point['latitude'][0:len(point['latitude']) - precision_reduction]
       point['longitude'] = point['longitude'][0:len(point['longitude']) - precision_reduction]
       point['elevation'] = point['elevation'][0:len(point['elevation']) - precision_reduction]


def distance_optimizer(etl_op):
    
    points_list = etl_op["gps_points"]
    gps_distance = list()
    # counts points meeting min separation criteria.
    # starts with one since we have to count the first point too
    count = 1
    

    for index, gps_point in enumerate(points_list):
        
        current_point = (gps_point['latitude'], gps_point['longitude'])

        while True:
            if index == len(points_list) - 1:
                #
                # break when last element detected, to avoid overrunning list using
                # the next index 
                #
                etl_op["current_points"] = count
                break

            next_point = (points_list[index+1]['latitude'], points_list[index+1]['longitude'])
            mydistance = distance.distance(current_point, next_point)
        
            if round(mydistance.m,1) < etl_op["gps_min_delta"]:
                points_list.pop(index+1)
                etl_op["delta_points_stripped"] += 1
                continue
            else:
                gps_distance.append(round(mydistance.m, 1))    
                count += 1
                #break the while
                break
