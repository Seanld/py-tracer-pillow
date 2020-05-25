# A very naive and basic project dedicated to making a 3D
# rendering engine that displays to the screen, via ray-tracing.
# |-> Written by Sean Wilkerson @ github.com/Seanld

from math import sin, cos, radians, sqrt
from random import randrange
from string import ascii_letters
from .vectors import Vector2, Vector3
from numpy import dot
from typing import List, Tuple



# Sorts objects farthest from origin first, closest last.
# NEEDS OPTIMIZATION!
def sortObjectsFarthest(origin, objectList):
    unsortedCopy = [x for x in objectList]
    maximum = Sphere(Vector3(), 0)
    newList = []

    while unsortedCopy:
        for x in unsortedCopy:
            if x.position.distanceTo(origin) >= maximum.position.distanceTo(origin):
                maximum = x
            newList.append(maximum)
            unsortedCopy.remove(x)
    
    newNewList = []
    for x in reversed(newList):
        newNewList.append(x)
    
    return newNewList


class Ray:
    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin = origin
        self.direction = direction
    
    def findT(self, t):
        Px = self.origin.x + (self.direction.x * t)
        Py = self.origin.y + (self.direction.y * t)
        Pz = self.origin.z + (self.direction.z * t)

        return Vector3(Px, Py, Pz)

class Color:
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
        self.rgb = (r, g, b)
    
    def change(self, rgb):
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        self.rgb = (self.r, self.g, self.b)

def ceiling(value):
    if value >= 255:
        return 255
    else:
        return value
    
def brighten(color: Color, rgb):
    newColor = Color(color.r, color.g, color.b)

    newColor.r = ceiling(newColor.r + rgb[0])
    newColor.g = ceiling(newColor.g + rgb[1])
    newColor.b = ceiling(newColor.b + rgb[2])

    newColor.rgb = (newColor.r, newColor.g, newColor.b)

    return newColor

class ImagePlane:
    # position: center of the plane
    # resolution: how many pixels wide and tall the plane is
    def __init__(self, position: Vector3, size: Vector2, resolution = None):
        self.position = position
        if resolution == None:
            self.resolution = size
        else:
            self.resolution = resolution
        self.size = size
        self.pixelSize = Vector2(size.x / self.resolution.x, size.y / self.resolution.y)
    
    def getPixelPositions(self) -> List[List[Vector3]]:
        Y = (self.position.y - (self.size.x / 2)) + (self.pixelSize.x / 2)
        Z = (self.position.z + (self.size.y / 2)) - (self.pixelSize.y / 2)
        startingPoint = Vector3(self.position.x, Y, Z)

        pixelPositions: List[List[Vector3]] = []

        for z in range(self.resolution.y):
            row: List[Vector3] = []

            for y in range(self.resolution.x):
                temp = Vector3(self.position.x, startingPoint.y + (y * self.pixelSize.x), startingPoint.z - (z * self.pixelSize.y))

                clone = temp.y
                temp.y = temp.x
                temp.x = clone

                row.append(temp)
            
            pixelPositions.append(row)
        
        return pixelPositions


class Space:
    def __init__(self):
        self.objects = []
        self.lights = []
    
    def addObject(self, _object):
        if type(_object) == PointLight:
            self.lights.append(_object)
        else:
            self.objects.append(_object)
    
    def deleteObject(self, id):
        i = 0

        while i < (len(self.objects) - 1):
            current = self.objects[i]

            if current.id == id:
                self.objects = self.objects[:i] + self.objects[i+1:]

    def calculateColorWithLight(self, objectToCalculate, origin):
        lightReaches = False
        totalLuminosity = 0

        for _light in self.lights:
            reflectionRay = Ray(origin, _light.position)

            for _object in self.objects:
                intersectionTest = _object.intersect(reflectionRay)

                if intersectionTest != None:
                    totalLuminosity += int((_light.intensity * (1 / ((origin.distanceTo(_light.position) / _light.radius) * 3))))
                    lightReaches = True
        
        if lightReaches:
            newColor = brighten(objectToCalculate.color, (totalLuminosity, totalLuminosity, totalLuminosity))
            # print("BEFORE", newColor.rgb)
            return newColor
        else:
            return objectToCalculate.color

class Camera:
    # position: physical location of camera.
    # screenDistance: distance of the screen from physical location of the camera.
    def __init__(self, position: Vector3 = Vector3(), space: Space = Space(),
        screenDistance: float = 10, screenRes: Vector2 = Vector2(100, 100),
        screenSize: Vector2 = Vector2(100, 100), bg = Color()):
        self.space = space

        self.position = position
        self.screenDistance = screenDistance
        self.screenRes = screenRes
        self.buffer = [[bg] * screenRes.x] * screenRes.y
        # self.vertices: List[str] = []
        self.screen = ImagePlane(Vector3(self.position.x + self.screenDistance, self.position.y, self.position.z), screenSize, screenRes)
        self.bg = bg

    # Renders and individual object; kept separate for readability purposes.
    def render(self):
        self.buffer = [[self.bg] * self.screenRes.x] * self.screenRes.y

        orderedObjects = sortObjectsFarthest(self.position, self.space.objects)

        allPixelPositions: List[List[Vector3]] = self.screen.getPixelPositions()
        ray: Ray = Ray(self.position, Vector3(0, 0, 0))

        y = 0

        finalBuffer = []

        for column in allPixelPositions:
            x = 0

            currentColumn = []

            for pixelPosition in column:
                ray.direction = pixelPosition
                currentData = self.buffer[y][x]

                for objectToRender in orderedObjects:
                    intersectResult = objectToRender.intersect(ray)
                
                    if intersectResult != None:
                        currentData = self.space.calculateColorWithLight(objectToRender, ray.findT(intersectResult[1]))
                        # print(currentData.rgb)
                        
                currentColumn.append(currentData)

                x += 1
                
                # THIS WAS FOR DEBUGGING, KEEPING IN CASE I NEED IT IN THE FUTURE!
                # self.vertices.append("({x}, {y}, {z} = {result}; ({pixelX}, {pixelY}))\n".format(x=pixelPosition.x, y=pixelPosition.y, z=pixelPosition.z, result=intersectResult, pixelX=x, pixelY=y))
            
            y += 1

            finalBuffer.append(currentColumn)
        
        self.buffer = finalBuffer

        return self.buffer

    # Absolute camera movement.
    def moveTo(self, position: Vector3):
        self.position = position
    
    # Relative camera movement.
    def moveBy(self, increment: Vector3):
        self.position += increment
        self.screen.position = Vector3(self.position.x + self.screenDistance, self.position.y, self.position.z)

    
class Object:
    def __init__(self, position: Vector3 = Vector3(), vertices: List[Vector3] = []):
        self.position = position
        self.vertices = vertices

    # Objects' vertices are relative to its position. To get absolute
    # vertices in relation to the space, use this method.
    def absoluteVertices(self) -> List[Vector3]:
        _absVertices = []

        for v in self.vertices:
            temp = Vector3(self.position.x + v.x, self.position.y + v.y, self.position.z + v.z)

            _absVertices.append(temp)
        
        return _absVertices



class PointLight:
    def __init__(self, position: Vector3, radius: float, intensity: 0.3):
        self.position = position
        self.radius = radius
        self.intensity = intensity


class Sphere (Object):
    def __init__(self, position: Vector3, radius: float, color=Color()):
        self.position = position
        self.radius = radius
        self.color = color
    
    # Check if `ray` intersects with Sphere.
    def intersect(self, ray: Ray) -> bool:
        dist = self.position - ray.origin

        distList = dist.asList()
        rayDirectionList = ray.direction.asList()

        a = dot(rayDirectionList, rayDirectionList)
        b = 2 * dot(rayDirectionList, distList)
        c = dot(distList, distList) - (self.radius ** 2)

        #print(a, b, c)

        discrim = b * b - 4 * a * c
        denominator = 2 * a

        if discrim < 0:
            return None
        
        if discrim == 0:
            return print("GLANCE!")

        discrimSquareRoot = sqrt(discrim)

        t1 = (b + discrimSquareRoot) / denominator
        t2 = (b - discrimSquareRoot) / denominator

        return (t1, t2)