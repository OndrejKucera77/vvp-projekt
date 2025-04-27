"""
Module containing the abstract parent class Sort.
"""

from abc import ABC, abstractmethod
from typing import List, Literal, Generator
from matplotlib.animation import Animation


class Sort(ABC):
    """
    Abstract class containing basic methods which every visualising sorting algorithm needs.
    Doesn't include any sorting algorithm which needs to be implemented in an inhereting class.

    Attributes:
        data - list of numbers (int/float) to sort
        order - desired order of the sorted list (ascending/descending), defaults to ascending
    
    Metods:
        set_data - sets data
        set_order - sets order
        animate - returns a visualisation animation of the sorting algorithm
    """


    def __init__(self, data: List[int|float] | str | None = None, order: Literal["ascending", "descending"] = "ascending") -> None:
        """
        Params:
            data - list of numbers to sort or a path to a file
            order - desired order of the sorted list
        """
        super().__init__()
        if data is not None:
            self.set_data(data)
        self.set_order(order)
    

    def set_data(self, data: List[int|float] | str) -> None:
        """
        Sets the data to be sorted. Data can be either in form of a list of numbers, or a string with the path
        to a file in which the data is saved.
        """
        if isinstance(data, list):
            # data jsou v listu čísel
            for i in data:
                if not isinstance(i, (int, float)):
                    raise TypeError("Data must be a list of numbers")
            self.data = data
        elif isinstance(data, str):
            # data jsou uložena v souboru
            with open(data, "r") as f:
                self.data = [float(x) for line in f for x in line.split()]
        else:
            raise TypeError("Data must be either a string or a list of numbers")


    def set_order(self, order: Literal["ascending", "descending"]) -> None:
        """
        Sets the desired order of the sorted data.
        """
        if order != "ascending" and order != "descending":
            raise TypeError("Order must be either 'ascending' or 'descending'")
        
        self.order = order
        self._order_int = (-1, 1)[self.order == "ascending"]

    
    def animate(self, speed: int|float = 0.5) -> Animation:
        # TODO
        self._check_anim_values(speed)
        
        iterator = self._sort_next()

        for i in iterator:
            print(i)


    def _check_anim_values(self, speed: int|float) -> None:
        """
        Checks whether all variables passed to `animate` have correct types and values.
        """
        if self.data is None:
            raise TypeError("Sorting data must be set")
        
        if not isinstance(speed, (int, float)):
            raise TypeError("Speed must be a number")
        elif speed <= 0:
            raise ValueError("Speed must have a positive value")

    
    @abstractmethod
    def _sort_next(self) -> Generator:
        """
        A generator function returning a dict of values to be shown in each frame of the algorithm's animation.
        """
        pass