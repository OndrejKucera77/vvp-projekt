"""
Module containing the Animation class.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from typing import List, Tuple


class Animation():
    """
    A class used to create the matplotlib's ArtistAnimation object.
    This class creates a visualization of a sorting algorithm from the visualization data, as a bar graph.

    Methods:
        set_style - sets the style (bar fill and edge colors etc.)
        create_anim - creates the animation
    """


    def __init__(self) -> None:
        """
        Creates an instance of this class and sets default style.
        """
        # TODO
        pass


    def set_style(self, style: dict) -> None:
        # TODO
        pass


    def create_anim(self, frames: List[dict], speed: int|float, figsize: Tuple[float, float] | None) -> ArtistAnimation:
        """
        Creates the visualization animation.
        
        Params:
            frames - list of frame data
            speed - delay between frames
            figsize - figure size (in inches)
        """
        # TODO
        self._check_anim_values(speed, figsize)


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