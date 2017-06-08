"""
main.py v 1.0.0
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import datetime

from lib import com_config, com_lcd, com_logger
from lib.driver import com_gps
from utils import POI

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# GPS
gps = com_gps.GPS()

# LCD
lcd = com_lcd.LCD()
# LCD Splash
lcd.splash(config['LOGGER']['levelconsole'], config['APPLICATION']['name'], config['APPLICATION']['author'], 'v' + config['APPLICATION']['version'])

# POI
poi = POI.POI()
bpoiimport = False
if bpoiimport:
    # Import RadarFile
    # Start time
    start = datetime.datetime.now()
    
    poi.importpoi()
    # Stop time
    end = datetime.datetime.now()
    logger.info('Import duration: ' + str(end - start))

while True:
    gps.getlocalisation()
    if gps.mode >= 2:
        listealerte = poi.getradararound(gps.latitude, gps.longitude, float(config['DATA']['distance']))
        if len(listealerte) > 0:
            print(listealerte[0][2])

logger.info('Application stop')
