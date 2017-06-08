"""
main.py v 1.0.0
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import datetime

from lib import com_config, com_logger

# Config
conf = com_config.Config()
# TODO : Delete for launch
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# Start time
start = datetime.datetime.now()

# Import RadarFile
# poi = POI.POI()
# poi.importpoi()

# Stop time
end = datetime.datetime.now()

logger.info('Import duration: ' + str(end - start))
logger.info('Application stop')
