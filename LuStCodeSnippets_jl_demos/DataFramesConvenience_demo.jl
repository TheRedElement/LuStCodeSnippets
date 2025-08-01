

#%%imports
using DataFrames
using Plots
using Random
using Revise

using LuStCodeSnippets_jl: DataFramesConvenience

#%%definitions

#%%demos
begin   #init DataFrame for demos
    rng = Xoshiro(0)
    nrows = 40
    df = DataFrame(
        :x1 => rand(rng, 1:5, nrows),
        :x2 => rand(rng, 1:3, nrows),
        :x3 => randn(rng, nrows),
        :x4 => split(randstring(rng, 'a':'z', nrows), r""),
    )
    # println(df)
end
begin #`value_counts()`
    println(DataFramesConvenience.value_counts(df, :x1; normalize=:none))
    println(DataFramesConvenience.value_counts(df, [:x1,:x2]; normalize=:frequency, sort=false))
    println(DataFramesConvenience.value_counts(df, [:x1,:x2]; normalize=:pdf, rev=true))
end