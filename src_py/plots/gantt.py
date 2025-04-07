
#%%imports
import polars as pl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from typing import Tuple

#%%definitions
def plot_gantt(
    df:pl.DataFrame,
    cmap:str,
    ax:plt.Axes,
    vmin:float=0.0, vmax:float=1.0,
    ) -> Tuple[Figure,plt.Axes]:
    """
        - function to plot a GANTT-chart based on a DataFrame of tasks

        Parameters
        ----------
            - `df`
                - `pl.DataFrame`
                - dataframe containing the tasks to plot
                - has to have the following columns
                    - `"task"
                    - `"start"
                    - `"end"
                    - `"category"
            - `cmap`
                - `str`
                - colormap to use for plotting individual categories
            
            - `ax`
                - `plt.Axes`
                - axes to plot into
            - `vmin`
                - `float`, optional
                - lower bound for colormap plotting
                - has to be between `0` and `1`
                - the default is `0.0`
            - `vmax`
                - `float`, optional
                - upper bound for colormap plotting
                - has to be between `0` and `1`
                - the default is `1.0`
        
        Raises
        ------

        Returns
        -------

    """

    colors = plt.get_cmap(cmap)(np.linspace(vmin,vmax,df["category"].n_unique(), endpoint=True))

    for cat, c in zip(sorted(df["category"].unique()), colors):
        ax.barh(
            df.filter(pl.col("category")==cat)["#"], 
            df.filter(pl.col("category")==cat)["duration"],
            left=df.filter(pl.col("category")==cat)["start"],
            height=.9,
            label=cat,
            color=c,
        )

    ax.set_yticks(
        range(len(df)),
        df["task"]
    )
    ax.margins(y=0)
    ax.legend(loc="upper left")
    ax.grid()


    ax.set_xlabel("Time [YYYY-MM]")


    return 