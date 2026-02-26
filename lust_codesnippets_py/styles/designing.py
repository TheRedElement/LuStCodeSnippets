#%%imports
import numpy as np
from plotly import graph_objects as go
from typing import Callable, List, Literal, Tuple, Union

#%%definitions
def design_colorscale(
    colorscale:List[Tuple[float,str]],
    testfunc:Union[Literal["gauss","linear"],Callable]="gauss",
    normalize:bool=True,
    noise:float=0.0,
    save:str=False,
    ) -> go.Figure:
    """creates a 2d heatmap colored with `colorscale`
    
    - useful for designing colormaps

    Parameters
        - `colorscale`
            - `List[Tuple[float,str]]`
            - color scale to visualize
            - each entry contains
                - stopping point (number from `0.0` to `1.0`)
                - associated color as as string supported by Plotly
        - `testfunc`
            - `Literal["gauss","linear"]`, `Callable`, optional
            - function to use for visualizing 2D heatmap
            - `"gaussian"` use gaussian
            - `"linear"` use linear gradient
            - if `Callable`
                - custom function to use for visualization
                - has to take two arguemnts (`x`, `y`)
            - the default is `"gauss"`
        - `normalize`
            - `bool`, optional
            - wether to normalize the heatmap
            - the default is `True`
        - `noise`
            - `float`, optional
            - amount of noise to add
            - the default is `0.0`
        - `save`
            - `str`, optional
            - file to save result to
            - the default is `False`
                - not saved

    Raises

    Returns
        - `fig`
            - `go.Figure`
            - plotly figure
    
    Dependencies
        - `numpy`
        - `plotly`
        - `typing`
    """
    x = np.linspace(-1,1,100)
    xx, yy = np.meshgrid(x,x)


    if callable(testfunc):
        #custom function
        zz = testfunc(xx, yy)
    else:
        #presets
        funcs = dict(
            gauss=np.exp(-0.5*((xx**2 + yy**2)**2)/0.1),
            linear=xx + yy,
        )
        assert testfunc in funcs.keys(), f"`testfunct` has to be one of {funcs.keys()}"
        zz = funcs[testfunc]


    if normalize: zz /= zz.max()
    zz += noise*np.random.randn(*zz.shape)

    #plotting
    fig = go.Figure(
        layout=dict(
            width=500,
            height=500,
        ),
    )
    fig.add_traces([
        dict(
            x=xx.flatten(),
            y=yy.flatten(),
            z=zz.flatten(),
            type="heatmap",
            colorscale=colorscale
        )
    ])
    if isinstance(save, str): fig.write_image(save)
    return fig
