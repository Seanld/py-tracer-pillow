from PIL import Image, ImageColor
from pt import *
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

imageSize = (800, 400)

cam = Camera(Vector3(0, 0, 0), screenDistance=400, screenSize=Vector2(imageSize[0], imageSize[1]), screenRes=Vector2(imageSize[0], imageSize[1]), bg=Color(230, 255, 255))



s1: Sphere = Sphere(Vector3(0, 200, 0), 100, Color(230, 0, 0))
s2: Sphere = Sphere(Vector3(-260, 520, 0), 80, Color(255, 102, 204))
l1: PointLight = PointLight(Vector3(-300, 300, 0), 300, 20)

cam.space.addObject(s1)
cam.space.addObject(s2)
cam.space.addObject(l1)
# cam.space.addObject(s3)

def renderFrame(size, cam, path):
    img = Image.new("RGB", size, "white")
    pixelMap = img.load()

    cam.render()

    y = 0
    for column in cam.buffer:
        x = 0

        for pixel in column:
            pixelMap[x, y] = pixel.rgb

            x += 1

        y += 1
    
    img.save(path)



idCounter = 0

movex = -260
movey = 0
movez = -70

for x in range(5):
    cam.moveTo(Vector3(movex, movey, movez))

    renderFrame(imageSize, cam, FILE_DIR + "/images/frame" + str(idCounter) + ".png")
    print("Frame " + str(idCounter) + " rendered...")

    movex += 50
    movey += 0
    movez += 30

    idCounter += 1

print("FINISHED RENDERING!")