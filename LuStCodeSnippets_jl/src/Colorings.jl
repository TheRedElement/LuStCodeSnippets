
"""

"""

module Colorings

#%%imports
using Plots

#import for extending

#%%exports
export colorcode

#intradependencies

#%%definitions
function colorcode(
    x::Vector;
    cmap::Union{Symbol,ColorPalette}=:plasma,
    clims::Union{Tuple,Nothing}=nothing,
    )
    #default parameters
    cmap = isa(cmap, Symbol) ? palette(cmap, 100) : cmap
    clims = isnothing(clims) ? (minimum(x),maximum(x)) : clims

    x_01 = (x .- clims[1])./(clims[2] - clims[1])
    # println(x_01)
    cidx = Int.(round.(x_01 .* (length(cmap)-1); digits=0)) .+ 1

    colors = cmap[cidx]
    return colors
end

end #module

