"""
Module containing the abstract parent class Sort.
"""

from abc import ABC, abstractmethod
from typing import List, Literal, Tuple, Generator
from matplotlib.animation import ArtistAnimation
from .animation import Animation


class Sort(ABC):
    """
    Abstract class containing basic methods which every visualising sorting algorithm needs.
    Doesn't include any sorting algorithm. This needs to be implemented in an inhereting class.

    Attributes:
        data - list of numbers (int/float) to sort
        order - desired order of the sorted list (ascending/descending), defaults to ascending
    
    Methods:
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
        self.animation = Animation()
    

    def set_data(self, data: List[int|float] | str) -> None:
        """
        Sets the data to be sorted. Data can be either in form of a list of numbers, or a string with a path
        to a file with the data. Data saved in a file should be valid float numbers divided by whitespace.
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
            raise ValueError("Order must be either 'ascending' or 'descending'")
        
        self.order = order
        self._order_int = (-1, 1)[self.order == "ascending"] # pro jednodušší porovnávání

    
    def animate(self, speed: int|float = 0.5, figsize: Tuple[float, float] | None = None) -> ArtistAnimation:
        """
        Creates the vizualization animation, as a bar graph.
        
        Params:
            speed - delay between frames
            figsize - figure size (in inches)
        """
        self._check_anim_values(speed, figsize)
        frames = [frame for frame in self._sort_next()]
        
        for frame in frames: # jen dočasné
            print(frame)
        
        return self.animation.create_anim(frames, speed, figsize)


    def _check_anim_values(self, speed: int|float, figsize: Tuple[float, float] | None) -> None:
        """
        Checks whether all variables passed to `animate` have correct types and values.
        """
        # data
        if self.data is None:
            raise ValueError("Sorting data must be set")
        
        # speed
        if not isinstance(speed, (int, float)):
            raise TypeError("Speed must be a number")
        elif speed <= 0:
            raise ValueError("Speed must have a positive value")
        
        # figsize (dále kontrolováno v matplotlib)
        if not isinstance(figsize, (tuple, type(None))):
            raise TypeError("Figure size must be a 2-tuple of floats")
        elif isinstance(figsize, tuple):
            if len(figsize) != 2:
                raise TypeError("Figure size must be a 2-tuple of floats")
            elif not isinstance(figsize[0], float) or not isinstance(figsize[1], float):
                raise TypeError("Figure size must be a 2-tuple of floats")

    
    @abstractmethod
    def _sort_next(self) -> Generator:
        """
        A generator function returning a dict of values to be shown in each frame of the algorithm's animation.
        
        These are the possible values:
            data - a (partially) sorted list of data
            compare - a 2-tuple with indexes of currently compared elements
            correct - a tuple of indexes of correctly sorted elements
        """
        pass