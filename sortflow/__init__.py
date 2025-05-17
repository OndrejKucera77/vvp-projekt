"""
This is the sortflow library. This library is used for creating vizualization animations
of sorting algorithms. Simply choose an algorithm and follow the documentation.

Modules:
- sort - contains the class Sort. To create your own sorting algorithm, make a class with Sort as its parent class.
- sort_algs - contains a few sorting algorithms.
- animation - contains the Animation class which is used to create the vizualization animation.
"""

from .sort import Sort
from .sort_algs import BubbleSort, InsertSort, SelectSort, QuickSort, MergeSort
from .animation import Animation

__all__: list[str] = ["Sort", "Animation", "BubbleSort", "InsertSort", "SelectSort", "QuickSort", "MergeSort"]