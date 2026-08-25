"""
extends [`DataFrames`](@ref)


Functions
    - [`df_to_pretty`](@ref)
    - [`value_counts`](@ref)
"""
module DataFramesExtension


#%%imports
using DataFrames
using PrettyTables

#import for extending

#intradependencies

#%%exports
export df_to_pretty
export value_counts

#%%definitions
"""
    df_to_pretty(df::DataFrame;
        backend::Symbol=:md,
        save::Union{Nothing,String}=nothing,
        kwargs...
        )::String

return a pretty print of a `df` for some `backend`

- adds type-based column alignments

See also
- [`PrettyTables.pretty_table`](@ref)

# Arguments
- `df`
    - `DataFrame` to prettify
- `backend`
    - backend to use when creating [`PrettyTables.pretty_table`](@ref)
- `save`
    - file to save the prettified version of the table to
    - the default is `nothing`
        - don't save
- `kwargs`
    - kwargs to be passed to [`PrettyTables.pretty_table`](@ref)

# Returns
- `pt`
    - `df` converted to a pretty `String`

# Extended help

## Dependencies
- [`PrettyTables.pretty_table`](@ref)
"""
function df_to_pretty(df::DataFrame;
    backend::Symbol=:md,
    save::Union{Nothing,String}=nothing,
    kwargs...
    )::String

    #type based column alignment
    alignments = Vector{Symbol}()
    for col in eachcol(df)
        if eltype(col) <: Number
            push!(alignments,:r)
        elseif eltype(col) <: String
            push!(alignments,:l)
        else
            push!(alignments,:l)
        end
    end

    #convert to latex string
    pt = pretty_table(String, df;
        backend=backend,
        alignment=alignments,
        row_labels=nothing,
        show_first_column_label_only=true,
        kwargs...
    )

    if !isnothing(save)
        open(save, "w") do f
            write(f, pt)
        end

    end

    return pt
end

"""
    function value_counts(
        df::DataFrames.DataFrame,
        subset::Union{Vector,Symbol,Nothing}=nothing;
        normalize::Symbol=:none,
        sort::Bool=true, rev::Bool=false,
        )::DataFrames.DataFrame

    imitates behavior of `[pandas.DataFrame.value_counts()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html)`

# Arguments
- `df`
    - dataframe the value-counts of which should be determined
- `subset`
    - subset of columns to use when counting unique combinations
    - the default is `nothing`
        - will consider all columns in `df`
- `normalize`
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
- `sort`
    - whether to sort by counts
    - if `false`
        - will sort by `subset` (via application of `groupby()`)
    - the default is `true`
- `rev`
    - whether to reverse the sorting (sort descending)
    - only applies if `sort==true`


# Returns
- `df_vc`
    - `DataFrames.DataFrame`
    - resulting dataframe displaying unique combinations of `subset` alongside their number of occurrence


# Extended help
## Dependencies
    - [`DataFrames`](@ref)

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
