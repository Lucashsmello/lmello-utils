import numpy as np

class Point(np.ndarray):
    def __new__(cls, x, y):
        return np.array([x, y]).view(cls)

    def __getattr__(self, attr):
        if attr == 'x':
            return self[0]
        if attr == 'y':
            return self[1]
        raise AttributeError("%r object has no attribute %r" %
                            (self.__class__.__name__, attr))

    def __setattr__(self, name, value):
        if name == 'x':
            self[0] = value
        elif name == 'y':
            self[1] = value
        else:
            super().__setattr__(name, value)

    def norm(self):
        return np.linalg.norm(self)

# Point = collections.namedtuple('Rect', 'x y')
