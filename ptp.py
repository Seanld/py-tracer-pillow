from PIL import Image
from pt import *
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

COLORS = {
    0: 1,
    1: 0
}

imageSize = (350, 500)

cam = Camera(screenDistance=50, screenSize=Vector2(350, 500), screenRes=Vector2(imageSize[0], imageSize[1]))\



s1: Sphere = Sphere(Vector3(0, 200, 0), 100)
# s2: Sphere = Sphere(Vector3(-80, 150, 20), 40)
# s3: Sphere = Sphere(Vector3(60, 145, 50), 60)

cam.space.addObject(s1)
# cam.space.addObject(s2)
# cam.space.addObject(s3)



img = Image.new("1", imageSize, "white")

renderedBuffer = cam.render()
y = 0
for column in renderedBuffer:
    x = 0

    for pixel in column:
        img.putpixel((x, y), COLORS[pixel])

        x += 1

    y += 1

img.save(FILE_DIR + "/sphere.png")