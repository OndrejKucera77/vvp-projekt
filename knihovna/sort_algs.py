"""
Module containing classes implementing different sorting algorithms.

Classes:
    BubbleSort
"""

from .sort import Sort
from typing import Generator


class BubbleSort(Sort):
    """
    This class implements an optimised bubble sort algorithm.
    """

    def _sort_next(self) -> Generator:
        yield {"data": self.data, "k": 0}
        
        n = len(self.data)
        right = n
        k = 0
        
        while right > 1:
            last_change = 0

            for i in range(right-1):
                k += 1
                yield {"data": self.data, "compare": (i, i+1), "correct": list(range(right, n)), "k": k}

                if self._order_int * (self.data[i] - self.data[i+1]) > 0:
                    self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                    last_change = i
                    yield {"data": self.data, "compare": (i, i+1), "correct": list(range(right, n)), "k": k}
            
            right = 0 if (last_change == 0) else (last_change + 1)
            yield {"data": self.data, "correct": list(range(right, n)), "k": k}