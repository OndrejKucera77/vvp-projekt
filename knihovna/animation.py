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
        pass