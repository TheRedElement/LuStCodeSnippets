"""functions to deal with color generation

- provides utilities to generate
    - sequences of colors
    - colormaps

Exceptions

Classes

Functions
    - `generate_categorical_cmap()` -- generates a custom (categorical) colormap

Other Objects
"""

#%%imports
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
from typing import Union

#%%definitions
def generate_categorical_cmap(
    colors:Union[list,tuple], res:int=256
    ) -> mcolors.ListedColormap:
    """returns a custom (categorical) colormap

    - function to generate a custom (categorical) colormap by passing a list of colors

    Parameters
        - `colors`
            - `list`, `tuple`
            - colors to use for values in ascending order
            - will assign each entry (`color`) to `res//len(colors)` values in the colormap
            - can contain strings or RGBA tuples
                - strings have to be named colors
        - `res`
            - `int`, optional
            - resolution of the colormap
            - has to be larger than `len(colors)` to get a good result
            - the default is `256`

    Raises

    Returns
        - `cmap`
            - `mcolors.ListedColormap`
            - generated colormap

    Dependencies
    ------------
        - `matplotlib`
        - `numpy`
    """

    #create custom color map

    #divide 
    npercolor = res//(len(colors))

    #template colormap
    viridis = plt.get_cmap("viridis", res)
    custom_colors = viridis(np.linspace(0, 1, res))
    
    #adjust colors
    for idx, c in enumerate(colors):
        #convert to RGBA tuple if named color is passed
        if isinstance(c, str): c = mcolors.to_rgba(c)

        custom_colors[idx*npercolor:, :] = c
    cmap = mcolors.ListedColormap(custom_colors)

    return cmap

def generate_colors(
    classes:Union[int,list,np.ndarray], 
    vmin:float=None, vmax:float=None, vcenter:float=None,
    cmap:Union[str,mcolors.Colormap]="plasma"
    ) -> np.ndarray:
    """returns a list of colors drawn from `cmap`

    - function to generate colors for a given set of unique classes
    - generates colors based on a `matplotlib` colormap

    Parameters
        - `classes`
            - `list`, `np.array`, `int`
            - the classes to consider
            - if an integer is passed, will be interpreted as the number of unique classes
            - does not have to consist of unique classes
                - will pick out the unique classes by itself
        - `vmin`
            - `float`, optional
            - `vmin` value of the colormap
            - useful if you want to modify the class-coloring
            - the default is `None`
                - will be set to `0.0`
        - `vmax`
            - `float`, optional
            - `vmax` value of the colormap
            - useful if you want to modify the class-coloring
            - the default is `None`
                - will be set to `len(classes)`
        - `vcenter`
            - `float`, optional
            - `vcenter` value of the colormap
            - useful if you want to modify the class-coloring
            - the default is `None`
                - will be set to `y_pred.mean()`
        - `cmap`
            - `str`, `mcolors.Colormap`, optional
            - name of the colormap or ListedColormap to use for coloring the different classes
            - the default is `'plasma'`

    Raises

    Returns
        - `colors`
            - `np.ndarray`
            - contains as many different colors as there are unique classes in `classes`
            - has shape `(ncolors,4)`

    Dependencies
        - `numpy`
        - `matplotlib`
        - `typing`
    """


    if isinstance(classes, int):
        classes_int = np.arange(0, classes, 1, dtype=int)    #initialize integer-class array
    else:
        classes_int = np.arange(0, np.unique(classes).shape[0], 1, dtype=int)    #initialize integer-class array

    if vmin is None:
        vmin = 0
    if vmax is None:
        if isinstance(classes, int):
            vmax = classes
        else:
            vmax = np.unique(classes).shape[0]
    if vcenter is None:
        vcenter = (vmin+vmax)/2
    ncolors = np.unique(classes).shape[0]

    #generate colors
    divnorm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    colors = plt.get_cmap(cmap, ncolors)
    colors = colors(divnorm(np.unique(classes_int)))
    return colors
