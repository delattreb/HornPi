"""
mainpio.py v 1.0.0
Autor: Bruno
Date : 09/06/2017
"""

import datetime

from lib import com_config, com_logger
from utils import POI

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# POI
poi = POI.POI()

# Import RadarFile
# Start time
start = datetime.datetime.now()

poi.importpoi()
# Stop time
end = datetime.datetime.now()
logger.info('Import duration: ' + str(end - start))

logger.info('Application stop')
