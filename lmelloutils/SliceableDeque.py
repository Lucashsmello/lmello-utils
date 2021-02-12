from collections import deque

class SliceableDeque(deque):
    def __getitem__(self, s):
        try:
            start, stop, step = s.start or 0, s.stop or sys.maxsize, s.step or 1
        except AttributeError:  # not a slice but an int
            return super().__getitem__(s)
        else:
            try:
                return list(itertools.islice(self, start, stop, step))
            except ValueError:  # incase of a negative slice object
                length = len(self)
                start, stop = length + start if start < 0 else start, length + stop if stop < 0 else stop
                return list(itertools.islice(self, start, stop, step))