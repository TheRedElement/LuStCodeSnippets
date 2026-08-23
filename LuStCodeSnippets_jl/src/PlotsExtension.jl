
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
export testplot

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

"""
    testplot(;
        colorway::Union{Nothing,Vector}=nothing,
        ls::Union{Symbol,Vector{Symbol}}=:auto,
        markers::Union{Symbol,Vector{Symbol}}=:auto,
        cmap::Union{Symbol,PlotUtils.ContinuousColorGradient}=:auto,
        hatches::Union{Symbol,Vector{Symbol}}=:x,
        )::Plots.Plot

creates a testplot for testing different styles/themes

# Arguments
- `colorway`
    - color palette to use
    - the default is `nothing`
        - uses active default colorway
- `ls`
    - linestyles to use for each series
    - similar to`colorway` but for linestyle
- `markers`
    - markerstyle to use for each series
    - similar to `colorway` but for markers
- `cmap`
    - colormap to use
- `hatches`
    - hatches to use for histograms
    - similar to `colorway` but for hatches

# Returns
- `p`
    - generated plot
"""
function testplot(;
    colorway::Union{Nothing,Vector}=nothing,
    ls::Union{Symbol,Vector{Symbol}}=:auto,
    markers::Union{Symbol,Vector{Symbol}}=:auto,
    cmap::Union{Symbol,PlotUtils.ContinuousColorGradient}=:auto,
    hatches::Union{Symbol,Vector{Symbol}}=:x,
    )::Plots.Plot

    #convert to matrices
    colorway = isa(colorway, Vector) ? vec(colorway) : colorway         #column vector for `String`
    hatches = isa(hatches, Vector) ? reshape(hatches, 1, :) : hatches
    ls = isa(ls, Vector) ? reshape(ls, 1, :) : ls
    markers = isa(markers, Vector) ? reshape(markers, 1, :) : markers

    #lineplot
    p1 = plot((1:9) .+ (1:10)';
        xlabel="X", ylabel="Y",
        seriestype=:line,
        ls=ls,
        alpha=1,
    )
    vline!(p1, [2,4,6];
        color=1, alpha=.2, label=""
    )
    plot!(p1, legendtitle="LEGTIT", legend_columns=5)

    #heatmap
    hm = heatmap(randn(50,50);
        xlabel="X", ylabel="Y",
        colorbar_title="Cbar",
        cmap=cmap,
    )

    #3d surface
    p2 = surface(1:5, 1:5, repeat(1:5, 1,5);
        colorbar_title="Cbar",
        cmap=cmap,
    )

    #scatter
    s1 = plot(randn(15), randn(15);
        zcolor=log.(rand(15) .+ 1),
        seriestype=:scatter,
        cmap=:coolwarm, colorbar_title="test"
    )
    plot!(s1, randn(15,6), randn(15,6);
        seriestype=:scatter, m=markers,
    )

    #histogram
    x = [randn(300) (randn(300) .* 0.5 .+ 2)]
    hg = histogram(x;
        fillstyle=hatches,
        linestyle=ls,
        color=[1 4], linecolor=[1 4],
    )

    #combine
    p = plot(p1, hm, p2, s1, hg;
    # p = plot(p1, s1,
        layout=@layout[ [a ; b] [c ; d] ; e],
        title="TITLE", plot_title="Suptitle",
        size=(1200,1200)
    )
    return p
end

end #module
