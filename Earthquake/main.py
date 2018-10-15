import io
import math
import ssl

import pandas as pd
import requests
from kivy.app import App
from kivy.config import Config
from kivy.core.image import Image as CoreImage
from kivy.graphics.context_instructions import Translate
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.boxlayout import BoxLayout

w = 1024
h = 512
cx = 0
cy = 0
ang = 0
Config.set('graphics', 'width', w)
Config.set('graphics', 'height', h)
zoom = 1
pi = math.pi
ssl._create_default_https_context = ssl._create_unverified_context
map = "https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/0,0," + str(
    zoom) + "." + str(cx) + "," + str(cy) + "," + str(ang) + "/" + str(w) + "x" + str(
    h) + "?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NDg1bDA1cjYzM280NHJ5NzlvNDMifQ.d6e-nNyBDtmQCVwVNivz7A#2/0.0/0.0/1/0/0.png?access_token=pk.eyJ1IjoicmlkZGlrOTYiLCJhIjoiY2ptejFmZWptM3d2NTNwbngyOGhpM2hpMSJ9.VBaWAglI_v22OxL59SbLXA"
earthquake = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"


# retrieve earthquakes data from us database
def earthquake_data(url):
    data = requests.get(url).content
    data = pd.read_csv(io.BytesIO(data), sep=",")
    return data


# retrieve a world map from mapbox api
def get_image(url):
    response = requests.get(url).content
    img = CoreImage(io.BytesIO(response), ext="png")
    return img


# convert coordiantes of earthquakes to web mercator
def mercX(x):
    lon = math.radians(x)
    lon_a = (256 / pi) * math.pow(2, zoom)
    lon_b = lon + pi
    return lon_a * lon_b


def mercY(y):
    lat = math.radians(y)
    # using -256 for invert the y axis because kivy y axis is inverted
    lat_a = (-256 / pi) * math.pow(2, zoom)
    lat_b = math.tan(pi / 4 + lat / 2)
    lat_c = pi - math.log(lat_b)
    return lat_a * lat_c


# draw the canvas
class Canvas(BoxLayout):
    def __init__(self, cx, cy, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        img = get_image(map)
        with self.canvas:
            # translate the center of canvas from bottom left corner to the center
            Translate(1024 / 2, 512 / 2)
            Rectangle(texture=img.texture, pos=(-1024 / 2, -512 / 2), size=(1024, 512))
            data = earthquake_data(earthquake)
            # create web mercators for the center of the map
            cx = mercX(cx)
            cy = mercY(cy)
            # loop trough the earthquakes data for drawing them on the map
            for i in range(0, len(data)):
                x = mercX(data["longitude"][i]) - cx
                y = mercY(data["latitude"][i]) - cy
                mag = data["mag"][i]
                # mag squared for better differentiation of the radius of circles on the map
                mag = math.pow(mag, 2) / 2
                # drawing the circles rapresentating the earthquakes using the magnitude for the radius and for translate the origin of the circle from bottom left to center
                Line(ellipse=(x - mag / 2, y - mag / 2, mag, mag))


class Main(App):
    def build(self):
        return Canvas(cx, cy)


Main().run()
