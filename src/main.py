"""
main.py v 1.0.0
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import datetime
import time

from lib import com_config, com_logger
from lib.driver import com_gps, com_lcd
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
logger.info('Splash screen')
# lcd.splash(config['LOGGER']['levelconsole'], config['APPLICATION']['name'], config['APPLICATION']['author'], 'v' + config['APPLICATION']['version'])

# POI
poi = POI.POI()


# TODO : Check in /boot if update file

def checkupdatepoifile():
    # config['RadarFile']['poi'] =
    pass


bpoiimport = True
if bpoiimport:
    # Import RadarFile
    # Start time
    start = datetime.datetime.now()
    
    poi.importpoi()
    # Stop time
    end = datetime.datetime.now()
    logger.info('Import duration: ' + str(end - start))

# TODO : Display image when GPS isn't connected
# Check GPS connection
logger.info('Check GPS connexion')
mode = 0
while mode < 2:
    mode, latitude, longitude = gps.getlocalisation()
    lcd.displaynogps()
lcd.displayoff()
logger.info('GPS connected')

while True:
    time.sleep(3)
    mode, latitude, longitude = gps.getlocalisation()
    if mode >= 2:
        listealerte = poi.getradararound(latitude, longitude, float(config['DATA']['distance']))
        if len(listealerte) > 0:
            for alerte in listealerte:
                logger.info('Name: ' + alerte[2] + ' Speed:' + str(alerte[3]))
                lcd.displayspeed(alerte[2], alerte[3], alerte[4])
