#%%imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import numpy as np
import re
from typing import Dict, List, Tuple, Union

#%%constants
#Line2D attributes related to visual style
MPL_STYLE_ATTRS:List[str] = [
    "color",
    "linestyle",
    "linewidth",
    "marker",
    "markerfacecolor",
    "markeredgecolor",
    "markeredgewidth",
    "alpha",
    "fillstyle",
    "dash_capstyle",
    "dash_joinstyle",
    "solid_capstyle",
    "solid_joinstyle",
]

#%%definitions
def pcolormesh_text(
    ax:plt.Axes,
    X:np.ndarray,
    cmap:Union[str,mcolors.Colormap]=None, nancolor:Union[str,Tuple]=None,
    norm:mcolors.Normalize=None,
    numformat:str=None,
    xoffset:float=0.5, yoffset:float=0.5,
    text_kwargs:Dict=None,
    ):
    """
        - function to add labels to the cells of a `ax.pcolormesh()`

        Parameters
        ----------
            `ax`
                - `plt.Axes`
                - axes to plot into
            - `X`
                - `np.ndarray`
                - 2d-array
                - contains the data associated with the labels
            - `cmap`
                - `str`, `mcolors.Colormap`, optional
                - colormap to use when drawing the labels
                - the default is `None`
                    - will use the reverese of `plt.rcParams["image.cmap"]`
            - `nancolor`
                - `str`, `Tuple`, optional
                - color to use for cells that contain `np.nan`
                - the default is `None`
                    - will be set to color in `cmap` corresponding to the lowest value
            - `norm`
                - `mcolors.Normalize`, optional
                - norm to apply to `X` for generating the colors
                - the default is `mcolors.Normalize()`
            - `numformat`
                - `str`, optional
                - formatter to apply for formatting the displayed numbers
                - the default is `None`
                    - will be set to `"%.1f"`
            - `xoffset`
                - `float`, optional
                - offset in x-direction
                - used to position text in cells or at gridpoints
                - the default is `+0.5`
                    - positioned in cell
            - `yoffset`
                - `float`, optional
                - offset in y-direction
                - used to position text in cells or at gridpoints
                - the default is `+0.5`
                    - positioned in cell
            - `text_kwargs`
                - `Dict`, optional
                - kwargs to pass to `ax.text()`
                - the default is `dict(ha="center", va="center")`

        Raises
        ------

        Returns
        -------

        Dependencies
        ------------
            - `matplotlib`
            - `numpy`
            - `typing`

        Comments
        --------
    """

    #default parameters
    if cmap is None:
        cmap = plt.rcParams["image.cmap"]
        cmap = cmap[:-2] if cmap[-2:]=="_r" else cmap+"_r"  #invert cmap to make labels readable
        cmap = plt.get_cmap(cmap)
    else:
        cmap = plt.get_cmap(cmap) if  isinstance(cmap, str) else cmap
    nancolor = cmap(0) if nancolor is None else nancolor
    norm = mcolors.Normalize() if norm is None else norm
    numformat = "%.1f" if numformat is None else numformat
    text_kwargs = dict(ha="center", va="center") if text_kwargs is None else text_kwargs
    if "ha" not in text_kwargs.keys(): text_kwargs["ha"] = "center"
    if "va" not in text_kwargs.keys(): text_kwargs["va"] = "center"

    #get colors for the text
    colorvals = X.copy()
    colorvals[np.isnan(colorvals)] = np.nanmin(colorvals)
    colors = cmap((norm(colorvals)>0.5).astype(np.float64))
    colors[np.isnan(X)] = mcolors.to_rgba(nancolor)

    #add text
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            
            #use specified color or generate based on `cmap`
            if "color" not in text_kwargs.keys():
                text_kwargs_use = text_kwargs.copy()
                text_kwargs_use["color"] = colors[i,j]
            else:
                text_kwargs_use = text_kwargs
            
            #render text
            ax.text(j+xoffset, i+yoffset, numformat%(X[i,j]),  **text_kwargs_use)

    return

def legend_line_map(
    fig:Figure,
    handels:List[Line2D], labels:List[str],
    header:str=None,
    x0:float=0.02, x1:float=0.25, y0:float=1.0,
    vsep:float=1.0, pad:float=0.01,
    topdown:bool=True,
    text_kwargs:Dict=None,
    header_kwargs:Dict=None,
    ) -> Figure:
    """
        - function to add a custom legend to a matplotlib figure
        - parses each label in `labels` for 2 parts
            - maps connects parts with a straight line matching the handle of that label
        
        Parameters
        ----------
            - `fig`
                - `Figure`
                - figure to add the legend to
            - `handels`
                - `List[Line2D]`
                - handles of the artists
                - used to define the style of the connecting lines
            - `labels`
                - `List[str]`
                - labels to use for the artists
                - will get split by `r"\s*->\s*"`
                    - an arrow (->) enclosed by 0 or more spaces
                - first match will be shown on the left of the line
                - second match will be shown to the right of the line
            - `header`
                - `str`, optional
                - header to show on top of the legend
                - split by the same pattern as `labels`
                - the default is `None`
                    - no header
            - `x0`
                - `float`, optional
                - has to be in interval [0,1]
                - western anchor point of the first label in relative figure coordinates
                - the default is `0.02`
            - `x1`
                - `float`, optional
                - has to be in interval [0,1]
                - western anchor point of the second label in relative figure coordinates
                - the default is `0.25`
            - `y0`
                - `float`, optional
                - has to be in interval [0,1]
                - vertical anchor point of the legend
                - if `topdown == True`
                    - northern anchor point
                - else
                    - southern anchor point
                - the default is `0.25`
            - `vsep`
                - `float`, optional
                - vertical separation in units of line-height
                - the default is `1.0`
            - `pad`
                - `float`, optional
                - padding between line and labels
                - relative figure coordinate units
                - the default is `0.01`
            - `topdown`
                - `bool`, optional
                - whether to plot the legend top-down (`True`) or bottom-up (`False`)
                - the default is `True`
            - `text_kwargs`
                - `Dict`, optional
                - kwargs to pass to `fig.text()` for legend entries
                - the default is `None`
                    - will be set to `dict()`
            - `header_kwargs`
                - `Dict`, optional
                - kwargs to pass to `fig.text()` for legend header
                - the default is `None`
                    - will be set to `dict(fontweight="bold")`

        Raises
        ------
            - `AssertionError`
                - if the parameters don't match the requirements

        Returns
        -------
            - `fig`
                - `Figure`
                - `fig` with added legend

        Dependencies
        ------------
            - `matplotlib`
            - `re`
            - `typing`

        Comments
        --------
    """

    #default parameters
    if text_kwargs is None: text_kwargs = dict()
    if header_kwargs is None: header_kwargs = dict(fontweight="bold")
    if "fontweight" not in header_kwargs.keys(): header_kwargs["fontweight"] = "bold"

    #checks
    assert len(handels)==len(labels), "`handels` and `labels` have to have the same length"
    assert (0<=x0)&(x0<=1), "`x0` has to be a number between 0` and `1` (relative figure coordinates)"
    assert (0<=x1)&(x1<=1), "`x1` has to be a number between 0` and `1` (relative figure coordinates)"
    assert (0<=y0)&(y0<=1), "`y0` has to be a number between 0` and `1` (relative figure coordinates)"

    #get renderer (to access artist bounding boxes)
    renderer = fig.canvas.get_renderer()

    #add new entry for each h-l pair
    ypos = y0           #init ypos
    ypos_header = y0    #init position of the header
    for (h, l) in zip(handels, labels):
        #extract legend entries
        labs = re.split(r"\s*->\s*", l)
        
        #add first label
        text1 = fig.text(x0, ypos, labs[0], ha="left", va="center", **text_kwargs)
        bbox1 = text1.get_window_extent(renderer=renderer).transformed(fig.transFigure.inverted())  #get bbox coordinates
        # bbox1_N = bbox1.get_points()[1,1]
        bbox1_E = bbox1.get_points()[1,0]
        # bbox1_S = bbox1.get_points()[0,1]
        # bbox1_W = bbox1.get_points()[0,0]
        lineheight = bbox1.height

        #add second label
        text2 = fig.text(x1, ypos, labs[1], ha="right", va="center", **text_kwargs)
        bbox2 = text2.get_window_extent(renderer=renderer).transformed(fig.transFigure.inverted())  #get bbox coordinates
        # bbox2_N = bbox2.get_points()[1,1]
        # bbox2_E = bbox2.get_points()[1,0]
        # bbox2_S = bbox2.get_points()[0,1]
        bbox2_W = bbox2.get_points()[0,0]


        #add line
        lprops = {k:h.properties()[k] for k in MPL_STYLE_ATTRS}
        line = Line2D([bbox1_E+pad, bbox2_W-pad], [ypos, ypos], transform=fig.transFigure, **lprops)
        fig.lines.append(line)

        #update `ypos` (proceed to next artist)
        if topdown:
            ypos -= vsep*lineheight
            #no update of ypos_heaeder (remains on top)
        else:
            ypos += vsep*lineheight
            ypos_header = ypos  #update header (to place on top)

    #add header
    if header is not None:
        #make sure header is on top
        if topdown: ypos_header += vsep*lineheight  
        
        #plot header
        headers = re.split(r"\s*->\s*", header)
        fig.text(x0, ypos_header, headers[0], ha="left",  va="center", **header_kwargs)
        fig.text(x1, ypos_header, headers[1], ha="right", va="center", **header_kwargs)
    
    return fig