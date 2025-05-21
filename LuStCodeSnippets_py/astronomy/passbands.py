#%%imports
import os
import polars as pl

#%%definitions
def get_passband_specs() -> pl.DataFrame:
    """
        - fuction to obtain a DataFrame of passband specifications

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
            - `df`
                - `pl.DataFrame`
                - contains passband specifications
                - each row is one passband

        Dependencies
        ------------
            - `os`
            - `polars`

        Comments
        --------
            - if you want to have an encoding-dict instead simply call `dict(zip(df["name"], df.select(pl.exclude("name")).to_numpy()))`
    """
    curdir = os.path.dirname(os.path.realpath(__file__)) +"/"
    df = pl.read_csv(f"{curdir}../../data/passband_specs.csv")
    
    return df