"""
Module containing the Animation class.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
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
        self.style = {
            "face_colors": {
                "unsorted": "#ff1e4c",
                "compare": "#FFEC1B",
                "sorted": "#23F01D"
            },
            "edge_colors": {
                "unsorted": "#b51536",
                "compare": "#B3A513",
                "sorted": "#1AB316"
            },
            "line_width": 3
        }


    def set_style(self, style: dict) -> None:
        # TODO
        pass


    def create_anim(self, frames: List[dict], speed: int|float = 0.5, figsize: Tuple[float, float] | None = None) -> ArtistAnimation:
        """
        Creates the visualization animation.
        
        Params:
            frames - list of frame data
            speed - delay between frames in seconds
            figsize - figure size (in inches)
        """
        self._check_anim_values(frames, speed, figsize)

        figure = plt.figure("Sorting algorithm animation", figsize=figsize)
        artists = []
        
        for frame in frames:
            artists.append(self._create_anim_frame(figure, frame))

        return ArtistAnimation(figure, artists, speed * 1000, blit=True)
    
    
    def _create_anim_frame(self, figure: Figure, frame: dict) -> BarContainer:
        """
        Create one frame of the animation.
        """
        n = len(frame["data"])
        x = range(n)
        y = frame["data"]

        # nastavení správných barev
        face_cols = [self.style["face_colors"]["unsorted"]] * n
        edge_cols = [self.style["edge_colors"]["unsorted"]] * n

        for i in range(n):
            if "compare" in frame and i in frame["compare"]:
                face_cols[i] = self.style["face_colors"]["compare"]
                edge_cols[i] = self.style["edge_colors"]["compare"]
            elif "correct" in frame and i in frame["correct"]:
                face_cols[i] = self.style["face_colors"]["sorted"]
                edge_cols[i] = self.style["edge_colors"]["sorted"]

        axes = figure.add_axes((0, 0, 1, 1))
        barc = axes.bar(x, y, facecolor=face_cols, edgecolor=edge_cols, linewidth=self.style["line_width"])
        return barc


    def _check_anim_values(self, frames: List[dict], speed: int|float, figsize: Tuple[float, float] | None) -> None:
        """
        Checks whether all variables passed to `create_anim` have correct types and values.
        """    
        # frames
        if not isinstance(frames, list):
            raise TypeError("Frames must be a list")
        else:
            for frame in frames:
                if not isinstance(frame, dict):
                    raise TypeError("Every frame must be a dict")
        
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
            elif not isinstance(figsize[0], (int, float)) or not isinstance(figsize[1], (int, float)):
                raise TypeError("Figure size must be a 2-tuple of floats")