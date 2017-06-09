"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

"""
Command:
stty -F /dev/ttyAMA0 9600

Now start GPSD:
gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
cgps -s
"""

import gpsd

from lib import com_logger


class GPS:
    def __init__(self):
        self.mode = 0
        self.sats = 0
        self.track = 0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.timeutc = ''
        self.latprecision = 0.0
        self.lonprecision = 0.0
        self.altprecision = 0.0
        self.hspeed = 0.0
        self.vspeed = 0.0

        # Logger
        self.logger = com_logger.Logger('GPS')
        
        # Connect to the local gpsd
        gpsd.connect()
    
    def gettime(self):
        ret = ''
        try:
            packet = gpsd.get_current()
            
            self.mode = packet.mode
            if self.mode >= 1:  # Check if mode 1 give time UTC
                self.timeutc = packet.time
                ret = str(self.timeutc[:-5].replace('T', ' ').replace('Z', ''))
        except:
            pass
        return ret
    
    def getlocalisation(self):
        
        try:
            # Get gps position
            packet = gpsd.get_current()
            
            # Debug info GPS
            self.logger.debug('mode:' + str(packet.mode))
            self.logger.debug('lon:' + str(packet.lon))
            self.logger.debug('lat:' + str(packet.lat))
            self.logger.debug('alt:' + str(packet.alt))
            self.logger.debug('hspeed:' + str(packet.hspeed))
            # logger.debug('vspeed:' + str(packet.speed_vertical()))
            self.logger.debug('lon +/-:' + str(packet.error['x']))
            self.logger.debug('lat +/-:' + str(packet.error['y']))
            self.logger.debug('alt +/-:' + str(packet.error['v']))
            self.logger.debug('sats:' + str(packet.sats))
            self.logger.debug('track:' + str(packet.track))
            self.logger.debug('time:' + str(packet.time))
            
            # See the inline docs for GpsResponse for the available data
            self.altitude = 0.0
            self.mode = packet.mode
            if self.mode >= 2:
                self.sats = packet.sats
                self.track = packet.track
                self.longitude = packet.lon
                self.latitude = packet.lat
                self.timeutc = packet.time
                self.hspeed = packet.hspeed
                self.lonprecision = packet.error['x']
                self.latprecision = packet.error['y']
        except Exception as e:
            self.logger.error('Exception:' + str(e))
        finally:
            return self.mode, self.latitude, self.longitude
