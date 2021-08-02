import requests
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

class  RidePlaner(object):
    def  __init__(self):
        self.api_key = "SIxrxBpid4EOWamRCnB0adoepHvfMrYv"
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    def calculate_path(self, origin_gps, destination_gps):
        url = "http://api.map.baidu.com/direction/v2/riding?origin={}&destination={}&ak={}".format(
            origin_gps, destination_gps, self.api_key
        )
        html = requests.get(url, headers = self.header)

        html_dir = json.loads(html.text, encoding='utf-8')['result']['routes'][0]['steps']

        origin_lngs, origin_lats = [], []
        markers_gps = ''
        for i in range(len(html_dir)):
            step_info = html_dir[i]
            origin_lng = step_info['stepOriginLocation']['lng']
            origin_lat = step_info['stepOriginLocation']['lat']
            origin_lngs.append(origin_lng)
            origin_lats.append(origin_lat)
            markers_gps += str(origin_lng)
            markers_gps += ','
            markers_gps += str(origin_lat)
            markers_gps += ';'
            paths = step_info['path'].split(';')[1: -1]
            for j in range(len(paths)):
                markers_gps += paths[j]
                markers_gps += ';'

        markers_gps += destination_gps.split(',')[1] + ',' + destination_gps.split(',')[0]
        center_lng = np.mean(np.array(origin_lngs))
        center_lat = np.mean(np.array(origin_lats))

        return center_lng, center_lat, markers_gps
    
    def save_path(self, center_lng, center_lat, markers_gps):
        url = "http://api.map.baidu.com/staticimage/v2?ak={}&center={},{}&width=1000&height=1000&zoom=17&paths={}&pathStyles=0xFF0000,5,1".format(
            self.api_key, center_lng, center_lat, markers_gps
        )
        image = requests.get(url, headers = self.header)

        f = open('/home/sbw/baidu_map/' + 'path_rideplan' + '.png', 'wb')
        f.write(image.content)
        f.close()

if __name__ == "__main__":
    origin_gps = '22.60808431791728,114.00273340573993'
    destination_gps = '22.599153684226555,114.00588269527528'
    
    planner = RidePlaner()
    center_lng, center_lat, markers_gps = planner.calculate_path(origin_gps, destination_gps)
    planner.save_path(center_lng, center_lat, markers_gps)
