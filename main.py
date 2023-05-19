import os

import numpy as np
from PIL import Image, ImageDraw
from pymongo import MongoClient


def merge_images(images, rows=None, cols=None):
    if rows is None and cols is None:
        rows = cols = int(np.sqrt(len(images)))

    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (max_width * cols, max_height * rows))

    y_offset = 0
    for i in range(0, rows):
        x_offset = 0
        for j in range(0, cols):
            new_im.paste(images[i * cols + j], (x_offset, y_offset))
            x_offset += max_width
        y_offset += max_height

    return new_im


print(os.environ['PATH'])

connection_string = os.environ['MONGODB_CONNECTION_STRING']
client = MongoClient(connection_string)
db = client["db_restaurant"]
collection = db["neighborhoods"]

documents = collection.find()
images = []

for document in documents:
    try:
        coordinates = document["geometry"]["coordinates"][0]

        lowest_x = coordinates[0][0]
        highest_x = coordinates[0][0]
        lowest_y = coordinates[0][1]
        highest_y = coordinates[0][1]

        for position in coordinates:
            if position[0] < lowest_x:
                lowest_x = position[0]
            if position[0] > highest_x:
                highest_x = position[0]
            if position[1] < lowest_y:
                lowest_y = position[1]
            if position[1] > highest_y:
                highest_y = position[1]

        for i in range(len(coordinates)):
            coordinates[i][0] = (coordinates[i][0] - lowest_x) * 200 / (highest_x - lowest_x)
            coordinates[i][1] = (coordinates[i][1] - lowest_y) * 200 / (highest_y - lowest_y)

        im = Image.new(mode="RGB", size=(200, 200))
        draw = ImageDraw.Draw(im)

        for i in range(len(coordinates) - 1):
            draw.line((coordinates[i][0], coordinates[i][1], coordinates[i + 1][0], coordinates[i + 1][1]),
                      fill=0x00ffff,
                      width=3)
        images.append(im)
    except TypeError:
        pass

merged_image = merge_images(images)
merged_image.show()
