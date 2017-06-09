"""
main.py v 1.0.0
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import datetime
import os
import shutil
import time
import zipfile

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
# region Import Radar file
if os.path.exists(config['RadarFile']['sourcefile']):
    logger.info('Found update radar file')
    logger.info('Unzip file')
    zip_ref = zipfile.ZipFile(config['RadarFile']['sourcefile'], 'r')
    zip_ref.extractall(config['RadarFile']['destdirectory'])
    zip_ref.close()
    logger.info('File unziped')
    
    # Start time
    start = datetime.datetime.now()
    
    poi.importpoi()
    # Stop time
    end = datetime.datetime.now()
    logger.info('Import duration: ' + str(end - start))
    logger.info('Delete radarfile zip')
    
    if os.path.exists(config['RadarFile']['sourcefile']):
        os.remove(config['RadarFile']['sourcefile'])
    logger.info('File deleted')
    if os.path.exists(config['RadarFile']['filedirectory']):
        shutil.rmtree(config['RadarFile']['filedirectory'])
    logger.info('Files deleted')
else:
    logger.info('No update radar file found')
# endregion

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
        else:
            logger.info('No radar')
