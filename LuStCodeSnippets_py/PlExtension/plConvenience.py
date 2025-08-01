
#%%imports
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