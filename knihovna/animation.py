"""
Module containing the Animation class.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from typing import List, Tuple, Dict


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
            "edge_width": 3,
            "background_color": "white",
            "bounds_color": "#DDD",
            "pivot_color": "black",
            "pivot_width": 3,
            "pivot_style": "-",
            "line_color": "black",
            "line_width": 2,
            "line_style": "--",
            "text_color": "black"
        }


    def set_style(self, style: Dict[str, any]) -> None:
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
        background_color: (color),
        bounds_color: (color),
        pivot_color: (color),
        pivot_width: (float),
        pivot_style: (style),
        line_color: (color),
        line_width: (float),
        line_style: (style),
        text_color: (color)
        }

        Colors should be in a valid matplotlib color format. Style should be a valid matplotlib line style, e.g. "dotted".
        """
        if not isinstance(style, dict):
            raise TypeError("Style must be a dictionnary")

        self._check_and_set_style_vals(style, {
            "face_colors.unsorted": "color",
            "face_colors.compare": "color",
            "face_colors.sorted": "color",
            "edge_colors.unsorted": "color",
            "edge_colors.compare": "color",
            "edge_colors.sorted": "color",
            "edge_width": "number",
            "background_color": "color",
            "bounds_color": "color",
            "pivot_color": "color",
            "pivot_width": "number",
            "pivot_style": "style",
            "line_color": "color",
            "line_width": "number",
            "line_style": "style",
            "text_color": "color"
        })


    def _check_and_set_style_vals(self, style_dict: Dict[str, any], keytypes: Dict[str, str]) -> None:
        """
        Receives a dict of style values to be set and a dict containing info on which key values should have which type.
        This method then checks whether all style values have the right type and if so, sets it.
        In case of nested dicts in the style dict, the keys in keytypes should be divided by a dot '.'.

        Params:
            style_dict - the dict with the style keys and values
            keytypes - the dict containing info oh the types of the key values
        """
        correct_types = {"color": (str, tuple), "number": (int, float), "style": (str)}
        
        for style_key in keytypes:
            keys = style_key.split(".")
            val = style_dict

            # klíče musí ve stylu být
            for key in keys:
                if key in val:
                    val = val[key]
                else:
                    break
            else:
                # pokud jsou, hodnota musí mít jeden z povolených typů
                if isinstance(val, correct_types[keytypes[style_key]]):
                    # a pak se nastaví
                    target = self.style
                    for key in keys[:-1]:
                        target = target[key] 
                    target[keys[-1]] = val


    def create_anim(self, frames: List[dict], title: str, speed: int|float = 0.5, repeat: bool = True, figsize: Tuple[float, float] | None = None) -> ArtistAnimation:
        """
        Creates the visualization animation.
        
        Params:
            frames - list of frame data
            speed - delay between frames in seconds
            repeat - if the animation should repeat
            figsize - figure size (in inches)

        Returns:
            ArtistAnimation - the animation
        """
        self._check_anim_values(frames, title, speed, repeat, figsize)

        fig = plt.figure(title, figsize)
        fig.set_facecolor(self.style["background_color"])
        fig.add_artist(Line2D([0.03, 0.97], [0.07, 0.07], color=self.style["line_color"], linestyle=self.style["line_style"], linewidth=self.style["line_width"]))
        fig.add_artist(Text(0.03, 0.03, "n = {}".format(len(frames[0]["data"])), color=self.style["text_color"]))
        fig.add_artist(Text(0.5, 0.03, title, horizontalalignment="center"))

        fig_axes = fig.add_axes((0, 0, 1, 1))
        fig_axes.set_frame_on(False)

        bar_axes = fig.add_axes((0, 0.08, 1, 0.9))
        bar_axes.set_frame_on(False)
        bar_axes.set_xticks([])
        bar_axes.set_yticks([])

        max_k = frames[-1]["k"]
        artists = []
        
        for frame in frames:
            artists.append(self._create_anim_frame(fig_axes, bar_axes, frame, max_k))

        return ArtistAnimation(fig, artists, speed * 1000, repeat=repeat, blit=True)
    
    
    def _create_anim_frame(self, fig_axes: Axes, bar_axes: Axes, frame: dict, max_k: int) -> List[Artist]:
        """
        Create a list of Artists to be shown in a new frame.

        Params:
            fig_axes - axes covering the whole figure
            bar_axes - axes where the barplot should be shown
            frame - current frame's data
            max_k - maximum iteration number
        
        Returns:
            List[Artist] - list with the artists
        """
        n = len(frame["data"])
        x = range(n)
        y = frame["data"]

        # nastavení správných barev sloupců
        face_cols = [self.style["face_colors"]["unsorted"]] * n
        edge_cols = [self.style["edge_colors"]["unsorted"]] * n

        for i in range(n):
            if "compare" in frame and i in frame["compare"]:
                face_cols[i] = self.style["face_colors"]["compare"]
                edge_cols[i] = self.style["edge_colors"]["compare"]
            elif "correct" in frame and i in frame["correct"]:
                face_cols[i] = self.style["face_colors"]["sorted"]
                edge_cols[i] = self.style["edge_colors"]["sorted"]

        bars = bar_axes.bar(x, y, facecolor=face_cols, edgecolor=edge_cols, linewidth=self.style["edge_width"])
        
        output = []
        bounds = (-0.5, n-0.5)

        if "bounds" in frame:
            bounds = (frame["bounds"][0] - 0.5, frame["bounds"][1] + 0.5)
            ylims = bar_axes.get_ylim()
            rect = bar_axes.add_artist(Rectangle((bounds[0], ylims[0]), bounds[1] - bounds[0], ylims[1] - ylims[0], color=self.style["bounds_color"]))
            output += [rect]
        
        output += list(bars)

        if "pivot" in frame:
            pivot = bar_axes.add_line(Line2D([bounds[0], bounds[1]], [frame["pivot"], frame["pivot"]], color=self.style["pivot_color"], linestyle=self.style["pivot_style"], linewidth=self.style["pivot_width"]))
            output += [pivot]

        text = fig_axes.text(0.97, 0.03, "k = {}/{}".format(frame["k"], max_k), horizontalalignment="right", color=self.style["text_color"])
        output += [text]
        
        return output


    def _check_anim_values(self, frames: List[dict], title: str, speed: int|float, repeat: bool, figsize: Tuple[float, float] | None) -> None:
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
        
        # title
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        
        # speed
        if not isinstance(speed, (int, float)):
            raise TypeError("Speed must be a number")
        elif speed <= 0:
            raise ValueError("Speed must have a positive value")

        # repeat
        if not isinstance(repeat, bool):
            raise TypeError("Repeat must be a boolean")
        
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