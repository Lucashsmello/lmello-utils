from collections import deque
import itertools

class SliceableDeque(deque):
    def __getitem__(self, s):
        if(isinstance(s, int)):
            return super().__getitem__(s)
        l = len(self)
        start, stop = s.start or 0, s.stop or l
        if(start < 0):
            start += l
        if(stop < 0):
            stop += l
        return list(itertools.islice(self, start, stop, s.step))

    def last(self, n: int = 1):
        if(n == 1):
            return super().__getitem__(-1)
        l = len(self)
        return list(itertools.islice(self, l-n, l))
