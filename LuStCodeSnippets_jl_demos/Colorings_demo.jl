
#%%imports
using Plots
using Random

using LuStCodeSnippets_jl: Colorings

#%%definitions

#%%demos
begin #colorcode()
    rng = Xoshiro(0)
    x = collect(rand(rng, range(-5,5,101), 101))
    colors = Colorings.colorcode(x)
    p = scatter(x; mc=colors)
end