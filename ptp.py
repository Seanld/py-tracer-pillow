from PIL import Image, ImageColor
from pt import *
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

COLORS = {
    0: 1,
    1: 0
}

imageSize = (500, 500)

cam = Camera(screenDistance=110, screenSize=Vector2(imageSize[0] * 4, imageSize[1] * 4), screenRes=Vector2(imageSize[0], imageSize[1]), bg=Color(50, 50, 255))



s1: Sphere = Sphere(Vector3(0, 200, 0), 100, Color(0, 0, 0))
s2: Sphere = Sphere(Vector3(-150, 150, 20), 40, Color(200, 40, 40))
s3: Sphere = Sphere(Vector3(120, 145, 80), 60, Color(40, 200, 40))

cam.space.addObject(s1)
cam.space.addObject(s2)
cam.space.addObject(s3)



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