import os

from PIL import Image, ImageDraw
from pymongo import MongoClient

print(os.environ['PATH'])

connection_string = os.environ['MONGODB_CONNECTION_STRING']
client = MongoClient(connection_string)
dbs = client.list_database_names()
print(dbs)

im = Image.new(mode="RGB", size=(200, 200))

draw = ImageDraw.Draw(im)
draw.line((100, 200, 200, 180), fill=0x00ffff, width=3)

im.show()
