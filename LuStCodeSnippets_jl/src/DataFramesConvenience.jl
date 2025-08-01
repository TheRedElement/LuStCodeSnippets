
"""
    - module implementing some convenience functions that are not available in `DataFrames`

    Constants
    ---------
    
    Structs
    -------
        - 

    Functions
    ---------
        - `value_counts()`

    Extended Functions
    ------------------

    Dependencies
    ------------
        - `DataFrames`

    Comments
    --------

    Examples
    --------
        - see [DataFramesConvenience_demo.jl](../../LuStCodeSnippets_jl_demos/DataFramesConvenience_demo.jl)
"""
module DataFramesConvenience
    

#%%imports
using DataFrames

#import for extending

#intradependencies

#%%exports
export value_counts

#%%definitions

#######################################
#helper functions


#######################################
#main functions
"""
    - function imitating behavior of `[pandas.DataFrame.value_counts()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html)`

    Parameters
    ----------
        - `df`
            - `DataFrames.DataFrame`
            - dataframe the value-counts of which should be determined
        - `subset`
            - `Vector`, `Symbol`, optional
            - subset of columns to use when counting unique combinations
            - the default is `nothing`
                - will consider all columns in `df`
        - `normalize`
            - `Symbol`, optional
            - how to normalize the counts
            - one of
                - `:none`
                    - no normalization
                    - raw counts
                - `:frequency`
                    - normalize to display frequency w.r.t. maximum value
                - `:pdf`
                    - normalize to display a pdf
                    - ensures that `sum(counts) == 1`
            - the default is `:none`
        - `sort`
            - `Bool`, optional
            - whether to sort by counts
            - if `false`
                - will sort by `subset` (via application of `groupby()`)
            - the default is `true`
        - `rev`
            - `Bool`, optional
            - whether to reverse the sorting (sort descending)
            - only applies if `sort==true`
            - the default is `false`


    Raises
    ------

    Returns
    -------
        - `df_vc`
            - `DataFrames.DataFrame`
            - resulting dataframe displaying unique combinations of `subset` alongside their number of occurrence

    Dependencies
    ------------
        - `DataFrames`

    Comments
    --------
"""
function value_counts(
    df::DataFrames.DataFrame,
    subset::Union{Vector,Symbol,Nothing}=nothing;
    normalize::Symbol=:none,
    sort::Bool=true, rev::Bool=false,
    )::DataFrames.DataFrame

    subset = isnothing(subset) ? names(df) : subset

    df_vc = combine(groupby(df, subset),
        subset .=> first .=> subset,
        nrow => :count
    )

    if normalize == :frequency
        transform!(df_vc,
            :count => ByRow(x -> x ./ maximum(df_vc[!,:count])) => :count;
            renamecols=true
        )
    elseif normalize == :pdf
        transform!(df_vc,
            :count => ByRow(x -> x ./ sum(df_vc[!,:count])) => :count;
            renamecols=true
        )
    end

    if sort
        sort!(df_vc, :count, rev=rev)
    end

    return df_vc
end

end #module
