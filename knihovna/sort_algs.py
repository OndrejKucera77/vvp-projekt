"""
Module containing classes implementing different sorting algorithms.

Classes:
    BubbleSort
    InsertSort
    SelectSort
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



class InsertSort(Sort):
    """
    This class implements a linear insertion sort algorithm.
    """

    def _sort_next(self) -> Generator:
        n = len(self.data)
        k = 0

        for i in range(1, n):
            yield {"data": self.data, "k": k, "correct": list(range(i))}
            moved = 0

            for j in range(i, 0, -1):
                k += 1
                yield {"data": self.data, "k": k, "compare": (j-1, j), "correct": list(range(i + moved))}

                if self._order_int * (self.data[j-1] - self.data[j]) > 0:
                    self.data[j], self.data[j-1] = self.data[j-1], self.data[j]
                    moved = 1
                    yield {"data": self.data, "k": k, "compare": (j-1, j), "correct": list(range(i + moved))}
                else:
                    break
        
        yield {"data": self.data, "k": k, "correct": list(range(n))}



class SelectSort(Sort):
    """
    This class implements a selection sort algorithm.
    """

    def _sort_next(self) -> Generator:
        yield {"data": self.data, "k": 0}

        n = len(self.data)
        k = 0

        for i in range(n-1):
            index = i
            
            for j in range(i+1, n):
                k += 1
                yield {"data": self.data, "k": k, "compare": (index, j), "correct": list(range(i))}

                if self._order_int * (self.data[index] - self.data[j]) > 0:
                    index = j
            
            if index != i:
                self.data[i], self.data[index] = self.data[index], self.data[i]
                yield {"data": self.data, "k": k, "compare": (index, i), "correct": list(range(i))}
            
            yield {"data": self.data, "k": k, "correct": list(range(i+1 if i != n-2 else n))}