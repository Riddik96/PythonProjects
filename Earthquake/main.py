import io
import tkinter as tk
import requests
from PIL import ImageTk, Image
root = tk.Tk()
root.geometry("1024x512")
map = "https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/0,0,1.0,0,60/1024x512?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NDg1bDA1cjYzM280NHJ5NzlvNDMifQ.d6e-nNyBDtmQCVwVNivz7A#2/0.0/0.0/1/0/0.png?access_token=pk.eyJ1IjoicmlkZGlrOTYiLCJhIjoiY2ptejFmZWptM3d2NTNwbngyOGhpM2hpMSJ9.VBaWAglI_v22OxL59SbLXA"
earthquake = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
earthquake_data = requests.get(earthquake)
earthquake_data = str(earthquake_data.content)
earthquake_data = earthquake_data.split(',')
print(earthquake_data[2])
raw_data = requests.get(map)
im = Image.open(io.BytesIO(raw_data.content))
image = ImageTk.PhotoImage(im)
cv = tk.Canvas()
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=image, anchor='nw')
root.mainloop()