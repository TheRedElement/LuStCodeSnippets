
#%%imports
import numpy as np
import polars as pl
from typing import Union, Literal, List

#%%definitions
def value_counts(
    df:pl.DataFrame,
    subset:Union[str,List[str],List[pl.Expr]]=None,
    normalize:Literal[None,"frequency","pdf"]=None,
    sort:bool=True, descending:bool=False,
    ) -> pl.DataFrame:
    """
        - function imitating behavior of `[pandas.DataFrame.value_counts()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html)`

        Parameters
        ----------
            - `df`
                - `pl.DataFrame`
                - dataframe the value-counts of which should be determined
            - `subset`
                - `str`, `List[str]`, `List[pl.Expr]` optional
                - subset of columns to use when counting unique combinations
                - the default is `None`
                    - will consider all columns in `df`
            - `normalize`
                - `Literal[None,"frequency","pdf"]`, optional
                - how to normalize the counts
                - one of
                    - `None`
                        - no normalization
                        - raw counts
                    - `"frequency"`
                        - normalize to display frequency w.r.t. maximum value
                    - `"pdf"`
                        - normalize to display a pdf
                        - ensures that `sum(counts) == 1`
                - the default is `None`
            - `sort`
                - `bool`, optional
                - whether to sort by counts
                - if `False`
                    - will sort by `subset` (via application of `groupby()`)
                - the default is `True`
            - `descending`
                - `bool`, optional
                - whether to reverse the sorting (sort descending)
                - the default is `False`


        Raises
        ------

        Returns
        -------
            - `df_vc`
                - `pl.DataFrame`
                - resulting dataframe displaying unique combinations of `subset` alongside their number of occurrence

        Dependencies
        ------------
            - `polars`

        Comments
        --------
    """
    #default parameters
    subset = df.columns if subset is None else subset

    df_vc = df.group_by(subset).agg(
        pl.len().alias("count")
    )

    if normalize is None:
        pass
    elif normalize == "frequency":
        df_vc = (df_vc
            .with_columns(pl.col("count")/pl.col("count").max())         
        )
    elif normalize == "pdf":
        df_vc = (df_vc
            .with_columns(pl.col("count")/pl.col("count").sum())         
        )
    else:
        raise ValueError(f"`count` has to be one of `None`, `'frequency'`, `'pdf'` but is {normalize}")

    if sort:
        df_vc = df_vc.sort(pl.col("count"), descending=descending)
    else:
        df_vc = df_vc.sort(subset, descending=descending)

    return df_vc

def cut(
    df:Union[pl.DataFrame,pl.LazyFrame],
    col:Union[pl.Expr,str], breaks:Union[List[float],int],
    format:str="%0.2f",
    alias:str=None,
    **cut_kwargs,
    ) -> Union[pl.DataFrame,pl.LazyFrame]:
    """
        - function extending on `pl.Expr().cut()`
        - makes sure that bins in resulting column are named consistently and easily sortable
            - especially important for plotting customizable histograms using `plt.bar()`

        Parameters
        ----------
            - `df`
                - `pl.DataFrame`, pl.LazyFrame`
                - dataframe to apply `cut()` to
            - `col`
                - `pl.Expr()`, `str`
                - column to apply `cut()` to
            - `breaks`
                - `List[float]`, `int`
                - breaks for creating the bins
                - if `List[float]`
                    - interpreted as bin bounds
                - if `int`
                    - interpreted as number of breaks to create (creates `breaks+2` bins)
            - `format`
                - `str`, optional
                - string formatting to use when creating the labels
                - necessary for consitent naming such that bins can be sorted easily
                - the default is `"%0.2f"
            - `alias`
                - `str`, optional
                - alias to give to the created column
                - passed to `pl.Expr().alias()`
                - the default is `None`
                    - will be set to `f"{col.meta.root_names()[0]}_cut"
            - `**cut_kwargs`
                - kwargs passed to `pl.Expr(col).cut()`

        Raises
        ------

        Returns
        -------
            - `df_cut`
                - `pl.DataFrame`, `pl.LazyFrame`
                - `df` with an additional column containing the bins

        Dependencies
        ------------
            - `numpy`
            - `polars`
        
        Comments
        --------
    """

    #default parameters
    if isinstance(col, str): col = pl.col(col)
    if isinstance(breaks, int): breaks = np.linspace(df.select(col).to_numpy().min(), df.select(col).to_numpy().max(), breaks)  #generate `breaks` breaks spanning the range of `col`
    if alias is None: alias = f"{col.meta.root_names()[0]}_cut"
    
    #deal with kwargs
    brackets = "(]"
    if "left_closed" in cut_kwargs.keys():
        if cut_kwargs["left_closed"]:
            brackets = "[)"

    #generate labels that make sense and can easily be sorted
    labs = [f"{brackets[0]}-inf,{format}{brackets[1]}"%(breaks[0])]+[f"{brackets[0]}{format},{format}{brackets[1]}"%(breaks[i],breaks[i+1]) for i in range(len(breaks)-1)]+[f"{brackets[0]}{format},+inf{brackets[1]}"%breaks[-1]]

    #apply pl.Expr().cut()
    df_cut = (df
        .with_columns(
            col.cut(breaks=breaks, labels=labs, **cut_kwargs).alias(alias)
        )
    )

    return df_cut