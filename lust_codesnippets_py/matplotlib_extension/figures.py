"""routines operating on matplotlib figures
"""

#%%imports
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
from typing import List, Tuple, Union

def merge_figures(
    figs:List[Union[Figure,str]],
    fig:Figure=None,
    temp_fname:str=None,
    ) -> Tuple[Figure, plt.Axes]:
    """merges a list of `matplotlib` figures into one figure

    - function to merge a list of matplotlib figures into one figure
    - done via `ax.imshow()`

    Parameters
        - `figs`
            - `List[Union[Figure,str]]`
            - list containing
                - matplotlib figures to be merged
                - paths to images of figures to be merged
            - has to be 1d!
        - `fig`
            - `Figure`, optional
            - matplotlib figure to plot the combined figures into
            - has to have at least as many `plt.Axes` as `Figures` in `figs`
            - will iterate over `fig.axes` to merge `figs`
            - the default is `None`
                - will autogenerate a figure
                - vertical stacking of `figs`
        - `temp_fname`
            - `str`, optional
            - filename to use for storing temporary files (images of elements in `figs`)
            - the default is `None`
                - will be set to `_temp.png`

    Raises
        - `ValueError`
            - if the shapes of `figs` and `fig.axes` don't mach

    Returns
        - `fig`
            - `Figure`
            - figure created by merging elements in `figs`
        - `axs`
            - `plt.Axes`
            - axes corresponding to `fig`

    Dependencies
        - `matplotlib`
        - `os`
        - `typing`
    """
    
    #default parameters
    if temp_fname is None: temp_fname = '_temp.png'
    if fig is None:
        fig, axs = plt.subplots(len(figs),1, subplot_kw=dict())
        for ax in fig.axes: ax.axis('off')
        fig.tight_layout(h_pad=0, w_pad=0)

    #check shapes
    if len(figs) > len(fig.axes):
        raise ValueError(
            f'`figs` can have a maximum length equal to the number of axis in `fig`. '
            f'The lengths are: {len(figs)=}, {len(fig.axes)=}'
        )

    #merging
    for idx, f in enumerate(figs):
        
        #check if path of figure was passed
        if isinstance(f, str):
            cur_fname = f
        else:
            cur_fname = temp_fname
            #temporarily save
            f.savefig(cur_fname)
        
        #load and plot into merged figure
        fig.axes[idx].imshow(plt.imread(cur_fname))
        
        #delete temporary file (if figure was passed)
        if not isinstance(f, str):
            os.remove(temp_fname)
    
    axs = fig.axes

    return fig, axs
    