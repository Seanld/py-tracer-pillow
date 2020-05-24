from PIL import Image, ImageColor
from pt import *
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

imageSize = (400, 200)

cam = Camera(Vector3(0, 0, 0), screenDistance=400, screenSize=Vector2(imageSize[0] * 2, imageSize[1] * 2), screenRes=Vector2(imageSize[0], imageSize[1]), bg=Color(230, 255, 255))



s1: Sphere = Sphere(Vector3(0, 200, 0), 100, Color(255, 0, 0))
s2: Sphere = Sphere(Vector3(-260, 520, 0), 80, Color(0, 0, 200))
l1: PointLight = PointLight(Vector3(-300, 300, 0), 300, 100)

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
            if pixel.rgb == (255, 20, 20):
                print("ITS HERE BITCH")
            pixelMap[x, y] = pixel.rgb

            x += 1

        y += 1
    
    img.save(path)



idCounter = 0

keyFrames = [
    Vector3(0, 200, 0),
    Vector3(0, 210, 0),
    Vector3(-10, 210, 0),
    Vector3(-20, 210, 0),
    Vector3(-40, 210, 0),
    Vector3(-80, 210, 0)
]

for pos in keyFrames:
    s1.position = pos

    renderFrame(imageSize, cam, FILE_DIR + "/images/frame" + str(idCounter) + ".png")

    print("Frame " + str(idCounter) + " rendered...")
    idCounter += 1

print("FINISHED RENDERING!")