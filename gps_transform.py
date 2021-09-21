from geopy import distance
import pandas as pd

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
                # break loop when last element detected
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
        #
        # debug code prints lat/lon and delta for points
        #
        #if index == 0:
        #    print("\npoint 0 lat lon : %s %s\npoint 1 lat lon : %s %s\ndistance (m) : %f\n" % 
        #            (gps_point['latitude'], gps_point['longitude'], dataList[index+1]['latitude'], dataList[index+1]['longitude'], round(mydistance.m, 1)))


    #
    # stats printing that probably belong somewhere else
    #
    print('GPS points stripped @ {gps_min_delta}m\t: {delta_points_stripped}'.format(**etl_op))  
    print('GPS points after distance strip\t: %d' % (len(points_list)))
    percent_reduction = round(100 * (etl_op["delta_points_stripped"] / etl_op["imported_points"]), 1)

    print('GPS points reduced %g percent' % (percent_reduction))  
    points_df = pd.DataFrame(gps_distance, index=None, columns=['Distance'])
    print('\nMean\t: %f\nMedian\t: %f\nMin\t: %f\nMax\t: %f' % (points_df.mean(), points_df.median(), points_df.min(), points_df.max()))

