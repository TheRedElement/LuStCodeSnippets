
#%%imports
import numpy as np
import plotly
from plotly import graph_objects as go
from IPython.display import display, HTML

#%%definitions
def latex_in_vscode():
    """
        - function to enable rendering of latex equations and symbols in VSCode
        -  wokraround from [tomas mazak](https://github.com/microsoft/vscode-jupyter/issues/8131#issuecomment-1589961116)

        Parameters
        ----------

        Raises
        ------
        
        Returns
        -------

        Dependencies
        ------------
            - `plotly`
            - `IPython`

        Comments
        -------- 
    """
    plotly.offline.init_notebook_mode()
    display(HTML(
        '<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_SVG"></script>'
    ))
    
    return

def add_hovergrid(
    fig:go.Figure,
    row:int, col:int,
    x:np.ndarray, y:np.ndarray,
    debug:bool=False,
    **kwargs
    ) -> go.Figure:
    """
        - function to add a grid for additional hover information to `fig`
        - implemented by means of a `go.Heatmap`
            - rendered on `zorder=-99`
            - all `np.nan` values
        
        Parameters
        ----------
            - `fig`
                - `go.Figure`
                - target figure instance
            - `row`
                - `int`
                - row of the target subplot
            - `col`
                - `int`
                - column of the target subplot
            - `x`
                - `np.ndarray`
                - 1d array specifying centerpoints of grid rows
                - has to have same shape as `y`
            - `y`
                - `np.ndarray`
                - 1d array specifying centerpoints of grid columns
                - has to have same shape as `x`
            - `debug`
                - `bool`, optional
                - whether to run in debug mode
                    - will display yhe generated grid as linear gradient in y
            - `**kwargs`
                - information to be displayed at each grid-point
                - each kwarg has to have the same shape as `x`
                    - one value for each grid-point


        Raises
        ------

        Returns
        -------
            - `fig`
                - `go.Figure`
                - modified version of `fig`

        Dependencies
        ------------
            - `numpy`
            - `plotly`
        
        Comments
        --------
            - a common way to generate a grid is via the following
            ```python
                xx, yy = np.meshgrid(x, y)
                xx, yy = xx.flatten(), yy.flatten()
            ```

    """

    #checks
    assert x.ndim == 1, "`x` can have a maximum of 1 dimension to work seamlessly with `go.Heatmap()`. consider calling `x.flatten()`"
    assert y.ndim == 1, "`y` can have a maximum of 1 dimension to work seamlessly with `go.Heatmap()`. consider calling `y.flatten()`"
    assert len(x) == len(y), "`x` and `y` have to have the same shape"
    for k, v in kwargs.items():
        assert len(x) == len(v), f"`{k}` has to have the same shape as `x` (one value for each coordinate in the grid)"


    #all z-values are `nan` (not relevant)
    z = np.linspace(0,1,len(x))
    if not debug: z*=np.nan     #hide if not in debugging mode

    #define template for things to show on hover
    cdata = np.stack(list(kwargs.values()), axis=-1)
    hovertemplate = "<br>".join([f"<b>{k}</b>:"+" %{customdata["+f"{i}"+"]}" for i,k in enumerate(kwargs.keys())])
    hovertemplate += "<extra></extra>"

    #add heatmap as grid for hover information
    hm = go.Heatmap(
        z=z, x=x, y=y,
        showscale=False, showlegend=False,  #never show
        zorder=-99,                         #move all the way to the back
        customdata=cdata,                   #add custom data
        hovertemplate=hovertemplate,        #add template
    )
    fig.add_trace(
        hm,
        row=row, col=col,
    )        

    return fig