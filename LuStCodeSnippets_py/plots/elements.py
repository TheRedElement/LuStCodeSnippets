#%%imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from typing import Dict, Union


#%%definitions
def pcolormesh_text(
    ax:plt.Axes,
    X:np.ndarray,
    cmap:Union[str,mcolors.Colormap]=None,
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
    norm = mcolors.Normalize() if norm is None else norm
    numformat = "%.1f" if numformat is None else numformat
    text_kwargs = dict(ha="center", va="center") if text_kwargs is None else text_kwargs
    if "ha" not in text_kwargs.keys(): text_kwargs["ha"] = "center"
    if "va" not in text_kwargs.keys(): text_kwargs["va"] = "center"

    #get colors for the text
    colors = cmap((norm(X)>0.5).astype(np.float64))

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