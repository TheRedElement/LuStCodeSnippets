
#%%imports
import numpy as np
import polars as pl
import re
from typing import Union, Literal, List

#%%definitions
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
    # edges = [[-np.inf,breaks[0]]]+[[breaks[i],breaks[i+1]] for i in range(len(breaks)-1)]+[[breaks[-1],np.inf]]
    #apply pl.Expr().cut()
    df_cut = (df
        .with_columns(
            col.cut(breaks=breaks, labels=labs, **cut_kwargs).alias(alias),
        )
    )

    return df_cut

def get_edges(
    s:pl.Series,
    unique:bool=True,
    lb:float=-np.inf, ub:float=+np.inf,
    ) -> np.ndarray:
    """
        - function to generate edges from a `pl.Categorical` column
        - will extract edges by
            - splitting labels with `","` as separator
            - stripping parentheses (`"(",")","[","]")`
            - converting numbers to `np.float64`

        Parameters
        ----------
            - `s`
                - `pl.Series`
                - input series to extract edges of
                - has to be of dtype `pl.Categorical`
                - has to have been generated from one of
                    - `pl.Expr().cut()` with default labels
                    - `plc.cut()`
            - `unique`
                - `bool`, optional
                - whether to return the unique edges
                - useful for aggregated columns/statistics
                - the default is `True`
                    - returns unique edges
            - `lb`
                - `float`, optional
                - lower bound to use instead of `-np.inf`
                - the default is `-np.inf`
                    - no change in the lower bound
            - `ub`
                - `float`, optional
                - upper bound to use instead of `np.inf`
                - the default is `np.inf`
                    - no change in the upper bound

        Raises
        ------
            - `AssertionError`
                - if `s` has a wrong dtype

        Returns
        -------
            - `edges`
                - `np.ndarray`
                - edges associated with `s`

        Dependencies
        ------------
            - `numpy`
            - `polars`
            - `re`

        Comments
        --------
            - especially useful in combination with `plt.stairs()`
    """
    
    #cehcks
    assert s.dtype==pl.Categorical, "`s` has to be a `pl.Categorical` column resulting from `plc.cut()` or `pl.Expr.cut()` (with default labels)"

    #split labels to obtain edges
    edges = np.concatenate(s
        .cast(pl.Utf8)
        .str.split(",")
        .to_numpy()
    )

    #make corrections to values
    edges = [re.sub(r"[\(\)\[\])]", "", edge) for edge in edges]    #remove brackets
    edges = np.array(edges).astype(np.float64)                      #convert to numpy and numeric values
    edges[edges==-np.inf]   = lb                                    #replace nonfinite values with bounds (if necessary)
    edges[edges==np.inf]    = ub                                    #replace nonfinite values with bounds (if necessary)
    if unique: edges = np.unique(edges)                             #return unique edges if requested
    
    return edges

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
