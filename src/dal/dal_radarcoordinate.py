"""
dal_gps v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""

from lib import com_logger


class DAL_radarcoordinate:
    def __init__(self, connection, cursor):
        # Log
        self.logger = com_logger.Logger()
        
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    def getaroundcoordinate(self, x1, x2, y1, y2):
        return self.cursor.execute(
            'SELECT latitude, longitude, name FROM radarcoordinate WHERE ' + 'latitude>' + str(x1) + ' and latitude<' + str(x2) + ' and longitude>' + str(y1) + ' and longitude<' + str(y2)).fetchall()
    
    """ Insert """
    
    def setcoordinate(self, lon, lat, speed, name, country):
        try:
            self.cursor.execute(
                'INSERT INTO radarcoordinate (longitude, latitude, speed, name, country) VALUES("' + str(lon) + '", "' + str(lat) + '", "' + str(speed) + '", "' + str(name) + '", "' + str(country) + '")')
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            self.logger.error(str(e))
    
    """ Delete """
    
    def delcoordinate(self):
        try:
            self.cursor.execute('DELETE FROM radarcoordinate')
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            self.logger.error(str(e))
