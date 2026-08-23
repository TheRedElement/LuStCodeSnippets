
"""

extends `Plots.jl`

Functions
- [`save_latex`](@ref) -- export some figure to LaTeX code (tikz)

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
"""
    save_latex(
        p::Plots.Plot,
        fname::String;
        preamble::Bool=true,
        background::Bool=false,
        thickness_scaling::Real=1.0,
        kwargs...
        )::Nothing

exports a [`Plots.jl`](@ref) to LaTeX code (`tikz`)

- requires to be run with [`Plots.pgfplotsx`](@ref) backend
- can be included in a LaTeX document using `\\input{<filename.tikz>}`
    ```latex
    \\resizebox\\linewidth}{!}{
        \\input{<filename.tikz>}
    }
    ```
- for styles from the [`LuStCodeSnippets`](@ref) package we recommend
    - `scale=2.0`

See also
- [`PlotsStyle`](@ref)

# Arguments
- `p`
    - plot to save
- `fname`
    - file to save to
    - has to have the extension `.tikz`
- `preamble`
    - whether to activate the recommended preamble
    - `false`: preamble commented
    - `true`: preamble uncommented
    - if you use colormaps, `preamble` **has** to be `true`
    - the default `true`
- `background`
    - whether to keep the background of `p`
    - `false`: background will be removed (transparent)
    - `true`: original background kept
    - the default is `false`
- `thickness_scaling`
    - scaling factor for plot elements upon saving
    - scaling of
        - font sizes
        - line thickness
    - recommended to set to `2.0` if you use [`PlotsStyle`](@ref)
    - the default is `1.0`
- `kwargs`
    - additional kwargs to pass to `plot!(p, kwargs...)` before saving

# Returns

# Extended help

## Raises
- `AssertionError`
    - if a wrong backend is used
    - if `fname` has the wrong extension

## Dependencies
- [`Logging`](@ref)
- [`Plots`](@ref)
- [`PGFPlotsX`](@ref)

"""
function save_latex(
    p::Plots.Plot,
    fname::String;
    preamble::Bool=true,
    background::Bool=false,
    thickness_scaling::Real=1.0,
    kwargs...
    )::Nothing

    @assert backend_name() == :pgfplotsx "only supported for `pgfplotsx` backend but got $(backend_name())"
    @assert fname[end-4:end] == ".tikz" "`fname` must end with `\".tikz\"` but got $(fname)"

    begin #adjust layout
        plot!(p; tex_output_standalone=false)   #to use with LaTeX's `\input{}`
        plot!(p; thickness_scaling=thickness_scaling)
        if !background
            plot!(p;
                background_color=nothing,
                background_color_outside=:match,
            )
        end
        plot!(p; kwargs...)
    end

    savefig(p, fname)

    begin #post-save replacements to make latex-native
        #read and replace
        f = open(fname, "r")
        lines = readlines(f)

        replacements = []
        if preamble
            push!(replacements, "% Recommended preamble"=>"% %Recommended preamble")
            push!(replacements, r"^%\s(.+)$"=>s"\1")
        end

        lines = replace.(lines, replacements...)
        close(f)
        #override old file
        f = open(fname, "w")
        write(f, join(lines, "\n"))
        close(f)
    end
end

end #module
