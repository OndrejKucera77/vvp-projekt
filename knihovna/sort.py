"""
Module containing the abstract parent class Sort.
"""

from abc import ABC, abstractmethod
from typing import List, Literal, Tuple, Generator
from matplotlib.animation import ArtistAnimation
from .animation import Animation
import copy


class Sort(ABC):
    """
    Abstract class containing basic methods which every visualising sorting algorithm needs.
    Doesn't include any sorting algorithm. This needs to be implemented in an inhereting class.

    Attributes:
        data - list of numbers (int/float) to sort
        order - desired order of the sorted list (ascending/descending), defaults to ascending
        style - the style of the animation (i.e. bar colors)
    
    Methods:
        set_data - sets data
        set_order - sets order
        set_style - sets the animation's style
        animate - returns a visualisation animation of the sorting algorithm
    """


    def __init__(self, data: List[int|float] | str | None = None, order: Literal["ascending", "descending"] = "ascending", style: dict | None = None) -> None:
        """
        Params:
            data - list of numbers to sort or a path to a file
            order - desired order of the sorted list
            style - a dict containing the style of the animation
        """
        super().__init__()
        
        if data is not None:
            self.set_data(data)
        self.set_order(order)

        self._animation = Animation()
        if style is not None:
            self._animation.set_style(style)
        self.style = self._animation.style
    

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
            self.data = copy.copy(data)
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
    

    def set_style(self, style: dict) -> None:
        """
        Sets the style of the animation. Only correctly provided values will be changed.

        Params:
            style - a dict of style values
        
        This is the dict's structure:
        {
        face_colors: {
            unsorted: (color),
            compare: (color),
            sorted: (color)
        }, edge_colors: {
            unsorted: (color),
            compare: (color),
            sorted: (color)
        }, edge_width: (float),
        line_width: (float),
        line_style: (style),
        line_color: (color),
        text_color: (color),
        background_color: (color)
        }

        Colors should be in a valid matplotlib color format. Style should be a valid matplotlib line style, e.g. "dotted".
        """
        self._animation.set_style(style)
        self.style = self._animation.style

    
    def animate(self, speed: int|float = 0.5, repeat: bool = True, figsize: Tuple[float, float] | None = None) -> ArtistAnimation:
        """
        Creates the visualization animation, as a bar graph.
        
        Params:
            speed - delay between frames in seconds
            repeat - if the animation should repeat
            figsize - figure size (in inches)
        
        Returns:
            ArtistAnimation - the animation
        """
        if self.data is None:
            raise ValueError("Sorting data must be set")
        
        frames = [copy.deepcopy(frame) for frame in self._sort_next()]
        return self._animation.create_anim(frames, speed, repeat, figsize)

    
    @abstractmethod
    def _sort_next(self) -> Generator:
        """
        A generator function returning a dict of values to be shown in each frame of the algorithm's animation.
        
        These are the possible values:
            data* - a (partially) sorted list of data
            k* - the iteration number (how many comparisons have been made)
            compare - a 2-tuple with indexes of currently compared elements
            correct - a list of indexes of correctly sorted elements
            bounds - a 2-tuple with the left and right bounds of currently processed data
            pivot - a number, exclusively for quicksort
        
        *these are required, the other are optional
        """
        pass