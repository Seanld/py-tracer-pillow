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
    
    def __repr__(self):
        return "<{x},{y}>".format(x=self.x, y=self.y)
    
    # Compares two Vector2 object positions.
    def compare(self, otherVector):
        return self.x == otherVector.x and self.y == otherVector.y

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

    def __repr__(self):
        return "<{x},{y},{z}>".format(x=self.x, y=self.y, z=self.z)
    
    def compare(self, otherVector):
        return self.x == otherVector.x and self.y == otherVector.y and self.z == otherVector.z