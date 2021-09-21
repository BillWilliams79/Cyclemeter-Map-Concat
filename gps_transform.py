from geopy import distance
import pandas as pd

#
# precision optimizer - drop 2 digits from lat, lon, and ele.
#
def precision_optimizer(points_list, precision_reduction):
   for gps_point in points_list:
       gps_point['latitude'] = gps_point['latitude'][0:len(gps_point['latitude']) - precision_reduction]
       gps_point['longitude'] = gps_point['longitude'][0:len(gps_point['longitude']) - precision_reduction]
       gps_point['elevation'] = gps_point['elevation'][0:len(gps_point['elevation']) - precision_reduction]


def distance_optimizer(points_list, minimum_distance):
    gps_distance = list()
    count = 0
    points_stripped = 0

    for index, gps_point in enumerate(points_list):
        
        current_point = (gps_point['latitude'], gps_point['longitude'])

        while True:
            if index == len(points_list) - 1:
                # break loop when last element detected
                #print(count)
                break

            next_point = (points_list[index+1]['latitude'], points_list[index+1]['longitude'])
            mydistance = distance.distance(current_point, next_point)
        
            if round(mydistance.m,1) < minimum_distance:
                points_list.pop(index+1)
                points_stripped += 1
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



    print('GPS points stripped @ %dm\t: %d' % (minimum_distance, points_stripped))  
    print('GPS points after distance strip\t: %d' % (len(points_list)))
    #percent_reduction = round(100 * (points_stripped / imported_points), 1)

   # print('GPS points reduced %g percent' % (percent_reduction))  
    points_df = pd.DataFrame(gps_distance, index=None, columns=['Distance'])
    print('\nMean\t: %f\nMedian\t: %f\nMin\t: %f\nMax\t: %f' % (points_df.mean(), points_df.median(), points_df.min(), points_df.max()))

