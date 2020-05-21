from PIL import Image, ImageColor
from pt import *
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

COLORS = {
    0: 1,
    1: 0
}

imageSize = (800, 500)

cam = Camera(Vector3(200, -400, 0), screenDistance=700, screenSize=Vector2(imageSize[0], imageSize[1]), screenRes=Vector2(imageSize[0], imageSize[1]), bg=Color(230, 255, 255))



s1: Sphere = Sphere(Vector3(0, 200, 0), 100, Color(230, 0, 0))
s2: Sphere = Sphere(Vector3(-260, 520, 0), 80, Color(255, 102, 204))

cam.space.addObject(s1)
cam.space.addObject(s2)
# cam.space.addObject(s3)



img = Image.new("RGB", imageSize, "white")
pixelMap = img.load()

renderedBuffer = cam.render()
y = 0
for column in renderedBuffer:
    x = 0

    for pixel in column:
        pixelMap[x, y] = pixel.rgb

        x += 1

    y += 1

img.save(FILE_DIR + "/sphere.png")