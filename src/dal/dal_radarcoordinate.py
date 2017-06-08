"""
dal_gps v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""


class DAL_radarcoordinate:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    def getCoordinate(self, mode):
        return self.cursor.execute(
            'SELECT mode, date, latitude, longitude, altitude, latitude_precision, longitude_precision, altitude_precision, hspeed FROM coordinate WHERE mode >= ' + str(
                mode) +
            ' ORDER by date').fetchall()
    
    """ Insert """
    
    def setCoordinate(self, lon, lat, speed, name, country):
        try:
            self.cursor.execute(
                'INSERT INTO radarcoordinate (longitude, latitude, speed, name, country) VALUES("' + str(lon) + '", "' + str(lat) + '", "' + str(speed) + '", "' + str(name) + '", "' + str(country) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
    
    """ Delete """
    
    def delCoordinate(self):
        try:
            self.cursor.execute('DELETE FROM radarcoordinate')
            self.connection.commit()
        except:
            self.connection.rollback()
