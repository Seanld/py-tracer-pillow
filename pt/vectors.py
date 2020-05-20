from math import sqrt
from typing import List

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Calculates distance between this Vector2 and another Vector2.
    def distanceTo(self, other):
        return sqrt(pow((self.x - other.x), 2) + pow((self.y - other.y), 2))

    def __add__(self, otherVector):
        return Vector2(self.x + otherVector.x, self.y + otherVector.y)
    def __sub__(self, otherVector):
        return Vector2(self.x - otherVector.x, self.y - otherVector.y)

    def asList(self) -> List[float]:
        return [self.x, self.y]

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    # Calculates distance between this Vector3 and another Vector3.
    def distanceTo(self, other):
        return sqrt(pow((self.x - other.x), 2) + pow((self.y - other.y), 2) + pow((self.z - other.z), 2))

    def __add__(self, otherVector):
        return Vector3(self.x + otherVector.x, self.y + otherVector.y, self.z + otherVector.z)
    def __sub__(self, otherVector):
        return Vector3(self.x - otherVector.x, self.y - otherVector.y, self.z - otherVector.z)

    def asList(self) -> List[float]:
        return [self.x, self.y, self.z]