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

# LCD
lcd = com_lcd.LCD()
# LCD Splash
logger.info('Splash screen')
# lcd.splash(config['LOGGER']['levelconsole'], config['APPLICATION']['name'], config['APPLICATION']['author'], 'v' + config['APPLICATION']['version'])

# POI
poi = POI.POI()

# Import Radar file
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
# GPS
gps = com_gps.GPS()
gps.mode = 0
while gps.mode < 2:
    gps.getlocalisation()
    lcd.displaygpsinformation(gps)
    time.sleep(1)
logger.info('GPS connected')

while True:
    gps.getlocalisation()
    if gps.mode >= 2:
        logger.debug('Hspeed: ' + str(gps.hspeed) + ' Sats: ' + str(gps.sats))
        listealerte = poi.getradararound(gps.latitude, gps.longitude, float(config['DATA']['distance']))
        if len(listealerte) > 0:
            # ListeAlerte: 0: latiture 1: longitude 2: name 3: speed 4 : Distance
            lcd.displayspeed(listealerte[0][2], listealerte[0][3], listealerte[0][4], gps)
        else:
            lcd.displaynoradar(gps)

# region Temp for debug
        if len(listealerte) > 0:
            cpt = 0
            for alerte in listealerte:
                logger.debug(str(cpt) + '. ' + alerte[2] + ' Speed: ' + str(alerte[3]) + ' Dist: ' + str(round(alerte[4], 2)))
                cpt += 1
# endregion
    else:
        lcd.displaynogps()
    time.sleep(2)
