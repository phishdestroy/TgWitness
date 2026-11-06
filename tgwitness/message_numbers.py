"""Missing message numbers stored as intervals, without expanding large gaps."""
from itertools import pairwise


class MissingNumbers:
    def __init__(self, ordered):
        self.ranges = [(a + 1, b) for a, b in pairwise(ordered) if b - a > 1]
        self.count = sum(stop - start for start, stop in self.ranges)

    def __len__(self):
        return self.count

    def __iter__(self):
        return self.sample()

    def sample(self, step=1):
        """Yield every nth absent number, preserving the offset between gaps."""
        offset = 0
        for start, stop in self.ranges:
            yield from range(start + (-offset % step), stop, step)
            offset += stop - start
