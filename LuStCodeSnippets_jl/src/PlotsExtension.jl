
"""

extends `Plots.jl`

Functions
- [`tre`](@ref) -- TheRedElement base style
- [`include_themes`](@ref) -- exposes custom themes to `Plots.jl` interface

Examples


"""
module PlotsExtension

#%%imports
using Logging
using Plots

#import for extending

#intradependencies

#%%exports
export save_latex

#%%constants

#%%definitions
function save_latex(
    p::Plots.Plot,
    fname::String;
    )

    @assert backend_name() == :pgfplotsx "only supported for `pgfplotsx` backend but got $(backend_name())"
    @assert fname[end-3:end] == ".tex" "`fname` must end with `\".tex\"` but got $(fname)"

    plot!(p;
        bg=nothing,
        bginside=nothing,
    )
    savefig(p, fname)

    begin #replacements to make latex-native
        #read and replace
        f = open(fname, "r")
        lines = readlines(f)
        lines = replace.(lines,
            r"^%\s(.+)$"=>s"\1",
        )
        lines = replace.(lines,
            "Recommended preamble"=>"% Recommended preamble",
        )
        close(f)
        #override old file
        f = open(fname, "w")
        write(f, join(lines, "\n"))
        close(f)
    end

end


end #module
