
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
    width="\\linewidth", height="0.3\\paperheight",
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
        content = read(f, String)
        content = replace(content,
            r",\swidth=\{[^\}]+"=>", width={\\linewidth",
        )
        close(f)
        #override old file
        f = open(fname, "w")
        write(f, content)
        close(f)
    end

end


end #module
