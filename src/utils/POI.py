"""
importPOI.py v 1.0.0
Auteur: Bruno DELATTRE
Date : 08/06/2017

Source: http://carte-gps-gratuite.fr/radars-et-points-d-interet.html
"""

import csv
import os
import sqlite3
from operator import itemgetter

import haversine

from dal import dal_radarcoordinate
from lib import com_config, com_logger


class POI:
    def __init__(self):
        # Log
        self.logger = com_logger.Logger()
        
        # Config
        conf = com_config.Config()
        self.config = conf.getconfig()
        
        # Get database name
        self.database = self.config['SQLITE']['database']
        
        # Database
        self.connection = sqlite3.Connection(self.database)
        self.cursor = self.connection.cursor()
    
    def importpoi(self):
        # DAL
        dal = dal_radarcoordinate.DAL_radarcoordinate(self.connection, self.cursor)
        
        self.logger.info('Delete database')
        dal.delcoordinate()
        self.logger.info('Import RadarFile')
        
        for root, dirs, files in os.walk(self.config['RadarFile']['directory']):
            for item in files:
                src_path = os.path.join(root, item)
                self.logger.info('Compute file: ' + item)
                speed = item[:-4]
                speed = speed[-3:]
                country = item[:3]
                with open(src_path, newline = '') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
                    for row in spamreader:
                        self.logger.debug('Insert row: ' + row[0] + ' ' + row[1] + ' ' + row[2])
                        lib = str.replace(row[2], '"', '')
                        try:
                            int(speed)
                        except ValueError:
                            speed = 0
                        dal.setcoordinate(float(row[0]), float(row[1]), float(speed), lib, country)
    
    def getradararound(self, latitude, longitude, distancealerte):
        lat_x1 = latitude - float(self.config['DATA']['range'])
        lat_x2 = latitude + float(self.config['DATA']['range'])
        
        lon_x1 = longitude - float(self.config['DATA']['range'])
        lon_x2 = longitude + float(self.config['DATA']['range'])
        
        # DAL
        dal = dal_radarcoordinate.DAL_radarcoordinate(self.connection, self.cursor)
        points = dal.getaroundcoordinate(lat_x1, lat_x2, lon_x1, lon_x2)
        
        listalerte = []
        
        for point in points:
            point1 = latitude, longitude,
            point2 = point[0], point[1]
            distance = haversine.haversine(point1, point2)
            if distance < distancealerte:
                point += (distance,)
                listalerte.append(point)
        
        if len(listalerte) > 0:
            listalerte.sort(key = itemgetter(3), reverse = False)
        
        return listalerte