import math
import csv
import gmplot
import numpy as np
import os
from math import degrees, atan2

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    if (compass_bearing >0) and (compass_bearing <=22.5):
        compass_bearing_normalized=22.5
    elif compass_bearing >=22.5 and compass_bearing <=45:
        compass_bearing_normalized=45
    elif compass_bearing >=45 and compass_bearing <=67.5:
        compass_bearing_normalized=67.5
    elif compass_bearing >=66.5 and compass_bearing <=90:
        compass_bearing_normalized=90
    elif compass_bearing >=90 and compass_bearing <=112.5:
        compass_bearing_normalized=112.5
    elif compass_bearing >=112.5 and compass_bearing <=135:
        compass_bearing_normalized=135
    elif compass_bearing >=135 and compass_bearing <=157.5:
        compass_bearing_normalized=157.5
    elif compass_bearing >=157.5 and compass_bearing <=180:
        compass_bearing_normalized=180
    elif compass_bearing >=180 and compass_bearing <=202.5:
        compass_bearing_normalized=202.5
    elif compass_bearing >=202.5 and compass_bearing <=225:
        compass_bearing_normalized=225
    elif compass_bearing >=225 and compass_bearing <=237.5:
        compass_bearing_normalized=237.5
    elif compass_bearing >=237.5 and compass_bearing <=260:
        compass_bearing_normalized=260
    elif compass_bearing >=260 and compass_bearing <=272.5:
        compass_bearing_normalized=272.5
    elif compass_bearing >=272.5 and compass_bearing <=285:
        compass_bearing_normalized=285
    elif compass_bearing >=285 and compass_bearing <=307.5:
        compass_bearing_normalized=307.5
    elif compass_bearing >=307.5 and compass_bearing <=330:
        compass_bearing_normalized=330
    elif compass_bearing >=330 and compass_bearing <=352.5:
        compass_bearing_normalized=352.5
    else:
        compass_bearing_normalized=0

    return compass_bearing_normalized

def distancenew(origin,destination):

    s_lat, s_lng=origin
    e_lat, e_lng=destination

    # approximate radius of earth in km
    R = 6373.0

    s_lat = s_lat*np.pi/180.0
    s_lng = np.deg2rad(s_lng)
    e_lat = np.deg2rad(e_lat)
    e_lng = np.deg2rad(e_lng)

    d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

    return round((2 * R * np.arcsin(np.sqrt(d)))*1000)


def sanitizeroute(filename,distance_threshold = 10,filter_threshold = 10):
    rowcount=0

    receivedfile='uploads/'+filename
    resultfile='uploads/result'+filename
    base=os.path.basename(receivedfile)
    os.path.splitext(base)
    filenamewithoutextention = os.path.splitext(base)

    threshold=int(distance_threshold)
    #if distance is less than the above threshold then the current location is ignored
    filter_threshold=int(filter_threshold)
    #if the skipped distance total is more than above threshold then the current location is not ignored
    total_distance=0
    skipped_distance=0
    latlist=[]
    lonlist=[]


    with open(receivedfile,'r') as csvfile, open(resultfile,'a') as research:
        reader = csv.reader(csvfile)
        for row in reader:
            stockrow=row[:]
            print("Stock row is {}".format(stockrow))
            print(len(row))
            for i in range(0,len(row)):
                row[i]=row[i].replace(" ","")
            print(" Edited row is {}".format(row))

            if (rowcount==0):
                print(row[0].replace('.','',1).isdigit())
                print(row[0])
                research.write(','.join(stockrow))
                research.write('\n')
                if row[0].replace('.','',1).isdigit():
                    print ((row[0],row[1]))
                    prev=(row[0],row[1])
                    rowcount += 1
                else:
                    rowcount=0


            elif row[0].replace('.','',1).isdigit()> 0:
                prevlat,prevlon=prev

                distanceinmeter=distancenew((float(prevlat),float(prevlon)),(float(row[0]),float(row[1])))
                total_distance=total_distance+distanceinmeter
                angle_bearing=calculate_initial_compass_bearing((float(prevlat),float(prevlon)),((float(row[0]),float(row[1]))))

                if(distanceinmeter>threshold) or (skipped_distance>=filter_threshold):
                    latlist.append(float(row[0]))
                    lonlist.append(float(row[1]))
                    skipped_distance=0
                    research.write(','.join(stockrow))
                    research.write('\n')
                    print ("Added {}{} --- distance apart {} with bearing {}".format(prev,(row[0],row[1]),distanceinmeter,angle_bearing))
                else:
                    skipped_distance=skipped_distance+distanceinmeter
                    print ("ignored {}{} --- distance apart {} with bearing {}".format(prev,(row[0],row[1]),distanceinmeter,angle_bearing))


                prev=(row[0],row[1])
                rowcount += 1

            else:
                research.write(','.join(stockrow))
                research.write('\n')


    print("Total distance is {}".format(total_distance))


    gmap1 = gmplot.GoogleMapPlotter(lonlist[0],latlist[0],18)
    gmap1.scatter( lonlist[:-2], latlist[:-2], '# FF0000',size = 20, marker = False )

    gmap1.plot(lonlist[:-2], latlist[:-2],'cornflowerblue', edge_width = 10)

    print(len(latlist))
    print(rowcount)
    reduction=round(100-((len(latlist))/rowcount)*100)
    print("{} percentage of points were reduced".format(round(100-((len(latlist))/rowcount)*100)))
    mapfile=filenamewithoutextention[0]+".html"
    gmap1.draw( mapfile )
    os.remove(receivedfile)

    return reduction

if __name__ == '__main__':
    # print_a() is only executed when the module is run directly.
    sanitizeroute('stc.kml',10,10)
