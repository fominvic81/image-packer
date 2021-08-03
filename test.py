from PIL import Image
import random
import os
import shutil

folder = './input'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

random.seed(1)

print('count: ', end='')

for i in range((int)(input())):
    image = Image.new('RGBA', (random.randint(64, 256), random.randint(64, 256)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255))
    image.save('./input/img' + str(i + 1) + '.png', 'PNG')