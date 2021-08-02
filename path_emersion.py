import requests
import rosbag
import sys

import numpy as np
import matplotlib.pyplot as plt

class PathEmersioner(object):
    def __init__(self):
        self.api_key = "XYACZ9uAnCtOCLoOL2vEKVRGjzk1l3bz"
        self.header = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    def save_path(self, center_lng, center_lat, markers_gps):
        url = "http://api.map.baidu.com/staticimage/v2?ak={}&coordtype=wgs84ll&center={},{}&width=1000&height=1000&zoom=18&paths={}&pathStyles=0xFF0000,5,1".format(
           self. api_key, center_lng, center_lat, markers_gps
         )

        image = requests.get(url, self.header)

        f = open('/home/sbw/baidu_map/' + 'path' + '.png', 'wb')
        f.write(image.content)
        f.close()
    
    def obtain_path(self, bag_file):
        bag = rosbag.Bag(bag_file, 'r')

        lngs = []
        lats = []
        markers_gps = ''

        bag_data = bag.read_messages('/ublox_gps/fix')
        for i, msg in enumerate(bag_data):
            if i % 5 == 0:
                longitude = msg[1].longitude
                latitude = msg[1].latitude
                lngs.append(longitude)
                lats.append(latitude)
                markers_gps += str(longitude)
                markers_gps += ','
                markers_gps += str(latitude)
                markers_gps += ';'

        markers_gps = markers_gps[:-1]
        center_lng = np.mean(np.array(lngs))
        center_lat = np.mean(np.array(lats))
        return center_lng, center_lat, markers_gps

if __name__ == "__main__":
    bag_file = sys.argv[1]
    emerisioner = PathEmersioner()
    center_lng, center_lat, markers_gps = emerisioner.obtain_path(bag_file)
    emerisioner.save_path(center_lng, center_lat, markers_gps)
