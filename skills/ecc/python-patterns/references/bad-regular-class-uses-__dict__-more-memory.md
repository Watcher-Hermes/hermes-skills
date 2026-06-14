# Bad: Regular class uses __dict__ (more memory)
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y