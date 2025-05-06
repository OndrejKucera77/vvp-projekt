"""
Module containing the Animation class.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.axes import Axes
from typing import List, Tuple


class Animation():
    """
    A class used to create the matplotlib's ArtistAnimation object.
    This class creates a visualization of a sorting algorithm from the visualization data, as a bar graph.

    Attributes:
        style - a dict setting the style of the animation (bar fill and edge colors etc.)

    Methods:
        set_style - sets the style
        create_anim - creates the animation as ArtistAnimation from matplotlib
    """


    def __init__(self) -> None:
        """
        Creates an instance of this class and sets default style.
        """
        self.style = {
            "face_colors": {
                "unsorted": "#FF1E4C",
                "compare": "#FFEC1B",
                "sorted": "#23F01D"
            },
            "edge_colors": {
                "unsorted": "#B51536",
                "compare": "#B3A513",
                "sorted": "#1AB316"
            },
            "line_width": 2.4,
            "line_style": "--",
            "line_color": "black",
            "text_color": "black",
            "background_color": "white"
        }


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
        }, line_width: (float),
        line_style: (style),
        line_color: (color),
        text_color: (color),
        background_color: (color)
        }

        Colors should be in a valid matplotlib color format. Style should be a valid matplotlib line style, e.g. "dotted".
        """
        if not isinstance(style, dict):
            raise TypeError("Style must be a dictionnary")
        
        if "face_colors" in style:
            s = style["face_colors"]
            if "unsorted" in s and isinstance(s["unsorted"], (str, tuple)):
                self.style["face_colors"]["unsorted"] = s["unsorted"]
            if "compare" in s and isinstance(s["compare"], (str, tuple)):
                self.style["face_colors"]["compare"] = s["compare"]
            if "sorted" in s and isinstance(s["sorted"], (str, tuple)):
                self.style["face_colors"]["sorted"] = s["sorted"]
        
        if "edge_colors" in style:
            s = style["edge_colors"]
            if "unsorted" in s and isinstance(s["unsorted"], (str, tuple)):
                self.style["edge_colors"]["unsorted"] = s["unsorted"]
            if "compare" in s and isinstance(s["compare"], (str, tuple)):
                self.style["edge_colors"]["compare"] = s["compare"]
            if "sorted" in s and isinstance(s["sorted"], (str, tuple)):
                self.style["edge_colors"]["sorted"] = s["sorted"]
        
        if "line_width" in style and isinstance(style["line_width"], (int, float)) and style["line_width"] >= 0:
            self.style["line_width"] = style["line_width"]
        
        if "line_style" in style and isinstance(style["line_style"], str):
            self.style["line_style"] = style["line_style"]
        
        if "line_color" in style and isinstance(style["line_color"], (str, tuple)):
            self.style["line_color"] = style["line_color"]
        
        if "text_color" in style and isinstance(style["text_color"], (str, tuple)):
            self.style["text_color"] = style["text_color"]
        
        if "background_color" in style and isinstance(style["background_color"], (str, tuple)):
            self.style["background_color"] = style["background_color"]


    def create_anim(self, frames: List[dict], speed: int|float = 0.5, figsize: Tuple[float, float] | None = None) -> ArtistAnimation:
        """
        Creates the visualization animation.
        
        Params:
            frames - list of frame data
            speed - delay between frames in seconds
            figsize - figure size (in inches)

        Returns:
            ArtistAnimation - the animation
        """
        self._check_anim_values(frames, speed, figsize)

        fig = plt.figure("Sorting algorithm animation", figsize=figsize)
        fig.add_artist(Line2D([0.03, 0.97], [0.07, 0.07], color=self.style["line_color"], linestyle=self.style["line_style"], linewidth=self.style["line_width"]))
        fig.add_artist(Text(0.03, 0.03, "n = {}".format(len(frames[0]["data"])), color=self.style["text_color"]))

        figAxes = fig.add_axes((0, 0, 1, 1))
        figAxes.set_facecolor(self.style["background_color"])

        barAxes = fig.add_axes((0, 0.08, 1, 0.9))
        barAxes.set_frame_on(False)
        barAxes.set_xticks([])
        barAxes.set_yticks([])

        artists = []
        
        for frame in frames:
            artists.append(self._create_anim_frame(figAxes, barAxes, frame))

        return ArtistAnimation(fig, artists, speed * 1000, blit=True)
    
    
    def _create_anim_frame(self, figAxes: Axes, barAxes: Axes, frame: dict) -> List[Artist]:
        """
        Create a list of Artists to be shown in a new frame.

        Params:
            figAxes - axes covering the whole figure
            barAxes - axes where the barplot should be shown
            frame - current frame's data
        
        Returns:
            List[Artist] - list with the artists
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

        bars = barAxes.bar(x, y, facecolor=face_cols, edgecolor=edge_cols, linewidth=self.style["line_width"])
        text = figAxes.text(0.97, 0.03, "k = {}".format(frame["k"]), horizontalalignment="right", color=self.style["text_color"])
        
        return list(bars) + [text]


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
        
        # figsize
        if not isinstance(figsize, (tuple, type(None))):
            raise TypeError("Figure size must be a 2-tuple of floats")
        elif isinstance(figsize, tuple):
            if len(figsize) != 2:
                raise TypeError("Figure size must be a 2-tuple of floats")
            elif not isinstance(figsize[0], (int, float)) or not isinstance(figsize[1], (int, float)):
                raise TypeError("Figure size must be a 2-tuple of floats")
            elif figsize[0] <= 0 or figsize[1] <= 0:
                raise ValueError("Figure size must be positive in both directions")