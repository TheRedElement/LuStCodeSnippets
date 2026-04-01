
#%%imports
import numpy as np
import polars as pl
import re
from typing import Union, Literal, List

#%%definitions
def append(
    df1:pl.DataFrame,
    df2:pl.DataFrame
    ) -> pl.DataFrame:
    """
        - function to append `df2` to `df1` even if the columns don't match
        - useful for i.e. appending values to a single or a subset of columns
        - will pad all other columns with `None`

        Parameters
        ----------
            - `df1`
                - `pl.DataFrame`
                - root dataframe
                    - used as reference for column ordering
                - `df2` will be appended to `df1`
            - `df2`
                - `pl.DataFrame`
                - extension dataframe
                - will be appended to `df1`

        Raises
        ------
            - `AssertionError`
                - if the input types are wrong

        Returns
        -------
            - `df`
                - `pl.DataFrame`
                - `df1` with appended `df2`
                - columns only present in `df1` will get filled with `None` in the `df2` rows
                - columns only present in `df2` will get filled with `None` in the `df1` rows

        Dependencies
        ------------
            - `numpy`
            - `polars`

        Comments
        --------
    """
    
    #checks
    assert isinstance(df1, pl.DataFrame)&isinstance(df2, pl.DataFrame), "this function does NOT work with `pl.LazyFrame`"

    #determine missing columns
    missing_df1 = list(set(df1.columns) - set(df2.columns))
    missing_df2 = list(set(df2.columns) - set(df1.columns))

    #pad dataframes with missing columns
    df1 = pl.from_dict({**{col:df1[col] for col in df1.columns}, **{col:[None]*df1.height for col in df2.columns if not np.isin(col, df1.columns)}})
    df2 = pl.from_dict({**{col:df2[col] for col in df2.columns}, **{col:[None]*df2.height for col in df1.columns if not np.isin(col, df2.columns)}})

    #cast to correct dtype
    df1 = df1.with_columns([pl.col(mc).cast(df2[mc].dtype) for mc in missing_df2])
    df2 = df2.with_columns([pl.col(mc).cast(df1[mc].dtype) for mc in missing_df1])
    
    #sort columns
    df2 = df2.select(df1.columns)
    
    #merge
    df = pl.concat([df1,df2])
    return df

def columns(
    df:Union[pl.DataFrame,pl.LazyFrame],
    sort:bool=True
    ) -> List[str]:
    """returns columns of `df`

    - convenience function to return columns no matter if `df` is a `pl.LazyFrame` or not

    Parameters
        - `df`
            - `pl.DataFrame`, `pl.LazyFrame`
            - the data frame to extract columns of
        - `sort`
            - `bool`, optional
            - whether to sort the returned columns
            - the default is `True`

    Raises

    Returns
        - `cols`
            - `List[str]`
            - columns of `df`

    Dependencies
        - `polars`
    """

    if isinstance(df, pl.LazyFrame):
        cols = df.collect_schema().names()
    else:
        cols = df.columns
    
    cols = sorted(cols) if sort else cols

    return cols

def cut(
    df:Union[pl.DataFrame,pl.LazyFrame],
    col:Union[pl.Expr,str], breaks:Union[List[float],int],
    format:str="%0.2f",
    alias:str=None,
    include_empty:bool=False,
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
            - `include_empty`
                - `bool`, optional
                - whether to include empty bins
                    - will be included as rows filled with `None` besides column with name `alias`
                - the default is `False`
                    - will drop bins that are empty
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
            col.cut(breaks=breaks, labels=labs, **cut_kwargs).alias(alias),
        )
    )

    #add missing labels if requested
    if (len(labs) != len(df_cut[alias].unique()))  & include_empty:
        missing = set(labs) ^ set(df_cut[alias].unique())
        df_cut = append(df_cut, pl.DataFrame(data=[m for m in missing], schema={alias:pl.Categorical}))

    return df_cut

def get_edges(
    s:pl.Series,
    unique:bool=True,
    lb:float=-np.inf, ub:float=+np.inf,
    ) -> np.ndarray:
    """returns edges for a `pl.Categorical` column

    - function to generate edges from a `pl.Categorical` column
    - will extract edges by
        - splitting labels with `","` as separator
        - stripping parentheses (`"(",")","[","]")`
        - converting numbers to `np.float64`
    - especially useful in combination with
        - `plc.cut()`
        - `pl.Expr.cut()` (with default labels)
        - `plt.stairs()`
    - empty bins will lead to a wrong number of edges!
    - you might have to remove `None` values of `s` before applying `get_edges()`

    Parameters
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
        - `AssertionError`
            - if `s` has a wrong dtype
            - is `s` contains `None`
                - will lead to issues when concatenating edges

    Returns
        - `edges`
            - `np.ndarray`
            - edges associated with `s`

    Dependencies
        - `numpy`
        - `polars`
        - `re`
    """
    
    #cehcks
    assert s.dtype==pl.Categorical, "`s` has to be a `pl.Categorical` column resulting from `plc.cut()` or `pl.Expr.cut()` (with default labels)"
    assert s.null_count() == 0, "remove all `None` values in `s` before applying `plc.get_edges()` (call `s.drop_nulls()`)"

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
