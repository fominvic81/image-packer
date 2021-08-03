import json
import math
import time
import os
import sys
import re
from PIL import Image

start = time.process_time()

class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class AtlasElement:

    def __init__(self, position: Vector, image: Image.Image, rotated: bool):
        self.position: Vector = position
        self.width: int = image.height if rotated else image.width
        self.height: int = image.width if rotated else image.height
        self.rotated: bool = rotated
        self.image: Image.Image = image

fileNames = os.listdir('./input')
images = []

area = 0
for fileName in fileNames:
    image = Image.open('./input/' + fileName)
    image.fileName = fileName
    images.append(image)
    area += image.width * image.height

maxSize = math.sqrt(area) * 0.1

images.sort(key=(lambda image: -image.width * image.height))

atlas: 'list[AtlasElement]' = []
oldProgress = -1
coef = 3000 / len(images)

places: 'list[Vector]' = [Vector(0, 0)]

width = 0
height = 0

imgIndex = 0
sys.stdout.flush()
while imgIndex < len(images):

    image = images[imgIndex]
    bestScore = -math.inf
    bestI = -1
    bestRotated = False

    for i in range(len(places)):
        place = places[i]

        for r in range(2):
            rotated = bool(r)
            w = image.height if rotated else image.width
            h = image.width if rotated else image.height
            if (place.x + w > maxSize or place.y + h > maxSize): continue

            nw = max(place.x + w, width)
            nh = max(place.y + h, height)
            score = width * height - nw * nh - (place.x + place.y) * coef

            if (score > bestScore):
                b = True
                for atlasEl in atlas:
                    if ((atlasEl.position.x < place.x + w) and (atlasEl.position.x + atlasEl.width > place.x) and (atlasEl.position.y < place.y + h) and (atlasEl.position.y + atlasEl.height > place.y)):
                        b = False
                        break
                if b:
                    bestScore = score
                    bestI = i
                    bestRotated = rotated

    if bestI == -1:
        maxSize *= 1.1
        continue

    place = places.pop(bestI)

    atlas.append(AtlasElement(Vector(place.x, place.y), image, bestRotated))

    w = image.height if bestRotated else image.width
    h = image.width if bestRotated else image.height

    width = max(width, place.x + w)
    height = max(height, place.y + h)

    places.clear()

    places.append(Vector(place.x, place.y + h))
    places.append(Vector(place.x + w, place.y))

    for atlasElA in atlas:
        x = 0
        y = 0
        for atlasElB in atlas:
            if (atlasElB.position.y < atlasElA.position.y + atlasElA.height and atlasElB.position.y + atlasElB.height >= atlasElA.position.y + atlasElA.height):
                if (atlasElB.position.x + atlasElB.width <= atlasElA.position.x):
                    x = max(x, atlasElB.position.x + atlasElB.width)
            if (atlasElB.position.x < atlasElA.position.x + atlasElA.width and atlasElB.position.x + atlasElB.width >= atlasElA.position.x + atlasElA.width):
                if (atlasElB.position.y + atlasElB.height <= atlasElA.position.y):
                    y = max(y, atlasElB.position.y + atlasElB.height)

        places.append(Vector(x, atlasElA.position.y + atlasElA.height))
        places.append(Vector(atlasElA.position.x + atlasElA.width, y))

    imgIndex += 1

    progress = math.floor((imgIndex / len(images)) * 100)
    if (progress != oldProgress):
        string = '\r['

        for i in range(progress):
            string += '='

        for i in range(100 - progress):
            string += '.'

        string += '] ' + str(progress) + '%'
        sys.stdout.write(string)
        oldProgress = progress


print('\n')

def sortAtlas(atlas: 'list[AtlasElement]'):
    def con(text): return int(text) if text.isdigit() else text
    def key(key): return [con(c) for c in re.split(r'(\d+)', key.image.fileName)]
    atlas.sort(key=key)

sortAtlas(atlas)

outImg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
atlasJSON = {}
for atlasEl in atlas:
    outImg.paste(atlasEl.image.rotate(90, expand=True) if atlasEl.rotated else atlasEl.image, (atlasEl.position.x, atlasEl.position.y))
    atlasJSON[atlasEl.image.fileName] = {
        'frame': {'x': atlasEl.position.x, 'y': atlasEl.position.y, 'w': atlasEl.width, 'h': atlasEl.height},
        'rotated': atlasEl.rotated,
    }
outImg.save('./output/atlas.png', 'PNG')

jsonFile = open('./output/atlas.json', 'w')
json.dump(atlasJSON, jsonFile, indent=4)

print('Count: ' + str(len(fileNames)))
print('Unused area: ' + str(format(100 - area/(width * height) * 100, '.3f') + '%'))
end = time.process_time()
print('time: ' + str(format(end - start, '.1f') + 's'))