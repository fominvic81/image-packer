import json
from PIL import Image
import os
import shutil

folder = './output'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

image = Image.open('./input/atlas.png')

file = open('./input/atlas.json')

atlas = json.load(file)

for fileName in atlas:
    info = atlas[fileName]
    img = image.crop((info['frame']['x'], info['frame']['y'], info['frame']['x'] + info['frame']['w'], info['frame']['y'] + info['frame']['h']))

    if (info['rotated']): img = img.rotate(270, expand=True)

    img.save('./output/' + fileName, 'PNG')