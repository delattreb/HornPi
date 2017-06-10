"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""
import math
import os
import time

from PIL import ImageFont

from lib.driver.oled.demo_opts import device
from lib.driver.oled.render import canvas


class LCD:
    def __init__(self):
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'FreeSans.ttf'))
        self.smallfont = ImageFont.truetype(font_path, 12)
        self.normalfont = ImageFont.truetype(font_path, 20)
        self.bigfont = ImageFont.truetype(font_path, 34)
    
    def splash(self, level, name, author, version):
        if int(level) > 10:
            i = 0
            while i <= 127:
                with canvas(device) as draw:
                    draw.rectangle((0, 0, device.width - 1, 45), fill = 0, outline = 1)
                    draw.text((4, 3), name, fill = "white", font = self.normalfont)
                    draw.text((5, 21), version, fill = "white", font = self.smallfont)
                    draw.text((5, 32), author, fill = "white", font = self.smallfont)
                    self.progressbarline(draw, 0, 53, 127, 10, i, 127, 2)
                i += 1
    
    @staticmethod
    def progressbarline(draw, x, y, width, height, value, max_value, interior = 2):
        # with canvas(device) as draw:
        interiormini = interior / 2
        
        # Exterior progressbar
        draw.rectangle((x, y, x + width, y + height), outline = 1, fill = 0)
        
        # Interior
        # Horizontal or vertical
        if width > height:  # Horizontal
            cal = round((((width - interior) * value) / max_value), 0)
            draw.rectangle((x + interiormini, y + interiormini, x + interiormini + cal, y + height - interiormini), outline = 0, fill = 1)
        else:  # Vertical
            cal = round((((height - interior) * value) / max_value), 0)
            draw.rectangle((x + interiormini, y + height - interiormini, x + width - interiormini, y + (height - cal) - interiormini), outline = 0, fill = 1)
    
    @staticmethod
    def progressbar(draw, x, y, width, height, value, max_value, thickness, space, interior = 2, border = True):
        interiormini = interior / 2
        
        # Exterior progressbar
        if border:
            draw.rectangle((x, y, x + width, y + height), outline = 1, fill = 0)
        
        # Interior
        # Horizontal or vertical
        if width > height:  # Horizontal
            totalblock = round((width - interior) / (thickness + space), 0)
            cal = int(round(((totalblock * value) / max_value), 0))
            index = x + interiormini
            for i in range(0, cal):
                draw.rectangle((index, y + interiormini, index + thickness, y + height - interiormini), outline = 0, fill = 1)
                index += (thickness + space)
        else:  # Vertical
            totalblock = round((height - interior) / (thickness + space), 0)
            cal = int(round(((totalblock * value) / max_value), 0))
            index = y + height - interiormini
            for i in range(0, cal):
                draw.rectangle((x + interiormini, index, x + width - interiormini, index - thickness), outline = 0, fill = 1)
                index -= (thickness + space)
    
    @staticmethod
    def progresscircle(draw, x, y, radius, thickness, maxsegments, segments, startangle, totalangle, direction):
        anglechange = (totalangle / maxsegments) * (math.pi / 180)
        i = startangle * (math.pi / 180)
        
        ax = x + (math.cos(i) * radius)
        ay = y - (math.sin(i) * radius)
        
        bx = x + (math.cos(i) * (radius + thickness))
        by = y - (math.sin(i) * (radius + thickness))
        
        for cpt in range(segments):  # for optimisation last process cpt is last value to segments new value
            i += direction * anglechange
            
            cx = x + (math.cos(i) * radius)
            cy = y - (math.sin(i) * radius)
            
            dx = x + (math.cos(i) * (radius + thickness))
            dy = y - (math.sin(i) * (radius + thickness))
            
            draw.polygon((ax, ay, bx, by, dx, dy), fill = 1, outline = 1)  # Color 1
            # self.oled.surface.polygon((ax, ay, cx, cy, dx, dy), fill = 1, outline = 1)  # Color 2
            
            ax = cx
            ay = cy
            
            bx = dx
            by = dy
    
    @staticmethod
    def displayoff():
        with canvas(device) as draw:
            draw.rectangle((0, 0, device.width, device.height), outline = 0, fill = 0)
    
    @staticmethod
    def displaygpsinformation(gps):
        with canvas(device) as draw:
            draw.text((1, 1), str.replace(str.replace(gps.timeutc, 'T', ' '), 'Z', ''), fill = "white")
            
            draw.text((1, 12), 'Lo:' + str(gps.longitude)[:8], fill = "white")
            draw.text((1, 22), 'La:' + str(gps.latitude)[:8], fill = "white")
            draw.text((1, 32), 'Al: ' + str(gps.altitude), fill = "white")
            
            draw.text((69, 12), '+/-:' + str(gps.lonprecision)[:5], fill = "white")
            draw.text((69, 22), '+/-:' + str(gps.latprecision)[:5], fill = "white")
            draw.text((69, 32), '+/-:' + str(gps.altprecision)[:5], fill = "white")
            
            draw.text((1, 44), 'SH:' + str(gps.hspeed), fill = "white")
            # draw.text((65, 44), 'SV:' + str(0), fill = "white")
            draw.text((1, 54), 'Sats: ' + str(gps.sats), fill = "white")
            draw.text((63, 54), 'track: ' + str(gps.track), fill = "white")
    
    def displaystart(self, cpt):
        memo = cpt
        for i in range(cpt):
            with canvas(device) as draw:
                draw.text((36, 5), '- START -', fill = "white")
                draw.text((55, 25), str(memo - i), fill = "white", font = self.bigfont)
                time.sleep(1)
    
    def displaynogps(self):
        with canvas(device) as draw:
            draw.text((0, 17), 'SIGNAL', fill = "white", font = self.bigfont)
    
    def displaynoradar(self):
        with canvas(device) as draw:
            draw.text((0, 17), 'COOL !', fill = "white", font = self.bigfont)
    
    def displayspeed(self, name, speed, distance):
        with canvas(device) as draw:
            draw.text((0, 0), name, fill = "white", font = self.smallfont)
            draw.text((0, 12), str(round(distance, 2)) + ' Km', fill = "white", font = self.normalfont)
            draw.text((0, 31), '' + str(speed), fill = "white", font = self.bigfont)
