"""
Module containing classes implementing different sorting algorithms. These classes
inherent from Sort.

Classes:
- BubbleSort
- InsertSort
- SelectSort
- QuickSort
- MergeSort
"""

from .sort import Sort
from typing import Generator, List


class BubbleSort(Sort):
    """
    This class implements an optimised bubble sort algorithm.
    """

    def _sort_next(self):
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

    def _sort_next(self):
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

    def _sort_next(self):
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



class QuickSort(Sort):
    """
    This class implements a quicksort algorithm. The pivot is chosen
    as the average of the first and the last element.
    """

    def _sort_next(self, left: int = 0, right: int|None = None, k: int = 0, correct: List[int] = []):
        if right is None:
            right = len(self.data) - 1
        elif left == right:
            correct.append(left)
            return

        pivot = (self.data[left] + self.data[right]) / 2
        l, r = left, right
        
        yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct}
        yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct, "pivot": pivot}

        while l < r:
            k += 1
            yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct, "pivot": pivot, "compare": (l, r)}
            
            if self._order_int * (self.data[l] - pivot) > 0 and self._order_int * (pivot - self.data[r]) > 0:
                self.data[l], self.data[r] = self.data[r], self.data[l]
                yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct, "pivot": pivot, "compare": (l, r)}
            
            if self._order_int * (self.data[l] - pivot) <= 0:
                l += 1
            if self._order_int * (pivot - self.data[r]) <= 0:
                r -= 1

        m = r - int(r >= l and self._order_int * (self.data[l] - pivot) > 0)

        for frame in self._sort_next(left, m, k, correct):
            k = frame["k"]
            yield frame
        for frame in self._sort_next(m+1, right, k, correct):
            k = frame["k"]
            yield frame
        
        yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct}



class MergeSort(Sort):
    """
    This class implements a recursive merge sort algorithm.
    """

    def _sort_next(self, left: int = 0, right: int|None = None, k: int = 0, correct: List[int] = []):
        if right is None:
            right = len(self.data) - 1
        elif left == right:
            correct.append(left)
            return
        
        yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct}

        m = (left + right) // 2

        for frame in self._sort_next(left, m, k):
            k = frame["k"]
            yield frame
        for frame in self._sort_next(m+1, right, k):
            k = frame["k"]
            yield frame

        i, j = left, m+1

        # in place merge
        while i <= m and j <= right:
            k += 1
            yield {"data": self.data, "k": k, "bounds": (left, right), "compare": (i, j), "correct": correct}

            if self._order_int * (self.data[i] - self.data[j]) > 0:
                self.data[i], self.data[i+1:j+1] = self.data[j], self.data[i:j]
                yield {"data": self.data, "k": k, "bounds": (left, right), "compare": (i, j), "correct": correct}
                m += 1
                j += 1
            
            i += 1
        
        yield {"data": self.data, "k": k, "bounds": (left, right), "correct": correct}