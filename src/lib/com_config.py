"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def setconfig(self):
        acquisitionduration = 10  # In hours
        
        # region Config
        # Version
        self.config['APPLICATION'] = {}
        self.config['APPLICATION']['name'] = 'HornPi'
        self.config['APPLICATION']['version'] = '1.0.0'
        self.config['APPLICATION']['author'] = '(C) - Bruno DELATTRE'
        self.config['APPLICATION']['splashduration'] = '1'
        
        # LOGGER
        self.config['LOGGER'] = {}
        self.config['LOGGER']['levelconsole'] = '20'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        self.config['LOGGER']['levelfile'] = '20'
        self.config['LOGGER']['logfile'] = 'log'
        self.config['LOGGER']['logfilesize'] = '1000000'
        
        # DATA
        self.config['DATA'] = {}
        self.config['DATA']['range'] = '0.01'
        self.config['DATA']['distance'] = '0.800'  # meter
        
        # Import RadarFile
        self.config['RadarFile'] = {}
        self.config['RadarFile']['directory'] = 'utils/RadarFile'
        
        # SQLite
        self.config['SQLITE'] = {}
        self.config['SQLITE']['database'] = 'database.db'
        
        # GPIO
        self.config['GPIO'] = {}
        
        # INPUT
        self.config['GPIO']['LED_ACQUISITION'] = '5'
        # INPUT
        self.config['GPIO']['INPUT_ACQUISITION'] = '27'
        
        # GPS
        self.config['GPS'] = {}
        self.config['GPS']['delay'] = '1'
        self.config['GPS']['nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPS']['delay']))))
        
        # endregion
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        with open(db_path, 'w') as configfile:
            self.config.write(configfile)
    
    def getconfig(self):
        self.config = configparser.RawConfigParser()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        self.config.read(db_path)
        return self.config