class Rectangle:
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive numbers")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Box(Rectangle):
    def __init__(self, width: float, height: float, depth: float):
        super().__init__(width, height)
        if depth <= 0:
            raise ValueError("Depth must be a positive number")
        self.depth = depth

    def volume(self) -> float:
        return self.width * self.height * self.depth


box = Box(2, 2, 3)
l = box.area()
v = box.volume()

print(f"Area: {l}, Volume: {v}")
