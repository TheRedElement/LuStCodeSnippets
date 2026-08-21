"""

    defines custom styles for `Plots.jl`


- resources
    - https://docs.juliaplots.org/latest/api/
    - https://docs.juliaplots.org/latest/generated/supported/
- `clorant"rgba(...)"` is compatible across all backends!
- prefer the functions over the themes
    - gives you more freedom to customize quickly

Functions
- [`tre`](@ref) -- TheRedElement base style
- [`include_themes`](@ref) -- exposes custom themes to `Plots.jl` interface

Examples
- see [PlotsStyle.jl](../tutorials/PlotsStyle.jl)

"""
module PlotsStyle

#%%imports
using Colors
using FixedPointNumbers
using JSON
using Logging
using Plots
using PlotThemes
using PlotUtils

#import for extending

#intradependencies
using  LuStCodeSnippets.LcsBase.Loaders: get_datapath

#%%exports
export tre
export fink
export lust
export include_themes

export mono_ls
export mono_markers
export mono_colors

#%%constants
const DATA_DIR = get_datapath()

#%%definitions
"""

    function tre(;
        theme::Symbol=:dark, cycle::Symbol=:cycle,
        colorway_override::Union{Nothing,AbstractVector}=nothing,
        cmap_override::Union{Nothing,AbstractMatrix,PlotUtils.ContinuousColorGradient,Symbol}=nothing,
        )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}

applies the TheRedElement base style to `Plots.jl` in the current session

- used as template for other style variations
- draws from `../_data/tre_PlotsJl.json` which is defined via `/styles/tre.json`

# Arguments
- `theme`
    - the theme to use
    - options are
        - `:dark`
        - `:light`
- `cycle`
    - mode to use for cycling through linestyles, markers, hatches, etc.
    - options are
        - `:cycle`
            - will cycle through the linestyles
            - every line consecutive line, marker, hatch, etc. will have a unique style
        - `:batch`
            - will batch similar linestyles together
            - consecutive lines, markes, hatches, etc. will have the same style
- `colorway_override`
    - override of the default tre colorway (colorway = palette)
    - vector elements have to be some valid form of `Plots.jl` color definition
        - I recommend hex representation
    - used to make quick customization to the coloration of a plot
    - used in downstream style variations (i.e., `lust()`)
- `cmap_override`
    - override of the default tre cmap (cmap = colorscale)
    - used to make quick customization to the coloration of a plot
    - used in downstream style variations (i.e., `lust()`)

See also
- [`fink`](@ref)
- [`lust`](@ref)

## Returns
- `colorway`
    - color palette used to cycle through when plotting
- `ls`
    - linestyles used to cycle through when plotting
- `markers`
    - markers used to cycle through when plotting
- `cmap`
    - colormap used in the style
- `hatches`
    - hatches used to cycle through when plotting

# Extended help
## Raises
- `AssertionError`
    - if some arguments don't comply with supported options

## Dependencies
- [`JSON`](@ref)
- [`Logging`](@ref)
- [`Plots`](@ref)
- [`PlotUtils`](@ref)
"""
function tre(;
    theme::Symbol=:dark, cycle::Symbol=:cycle,
    colorway_override::Union{Nothing,AbstractVector}=nothing,
    cmap_override::Union{Nothing,AbstractMatrix,PlotUtils.ContinuousColorGradient,Symbol}=nothing,
    )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}


    @assert in(theme, [:dark,:light]) "`theme` has to be one of `:dark`, `:light` but got $(theme)"
    @assert in(cycle, [:cycle,:batch]) "`cycle` has to be one of `:cycle`, `:batch` but got $(cycle)"

    #load style from json
    style = JSON.parsefile(joinpath(DATA_DIR, "tre_PlotsJl.json"))

    begin #deal with overrides
        if isnothing(cmap_override)
            cmap = hcat(style[:colors][:c_plot_cmap][theme]...)
            cgrad_lcs = cgrad(cmap[2,:], cmap[1,:])
        elseif isa(cmap_override, Matrix)
            cmap = cmap_override
            cgrad_lcs = cgrad(cmap[2,:], cmap[1,:])
        elseif isa(cmap_override, PlotUtils.ContinuousColorGradient)
            cgrad_lcs = cmap_override
        elseif isa(cmap_override, Symbol)
            cgrad_lcs = cgrad(cmap_override)
        end

        colorway::Vector{String} = isnothing(colorway_override) ? style[:colors][:c_plot_colorway][theme] : colorway_override
        hatches = Symbol.(style[:hatches][cycle])
        ls = Symbol.(style[:line][:dash][cycle][1:length(colorway)])
        markers = Symbol.(style[:marker][:symbol][cycle])
    end

    @debug cgrad_lcs typeof(cgrad_lcs)
    @debug colorway typeof(colorway)
    @debug hatches
    @debug ls
    @debug markers

    begin #layout
        default(
            size=(900,500),
            top_margin=6Plots.mm,
            bottom_margin=6Plots.mm,
            left_margin=6Plots.mm,
            right_margin=6Plots.mm,
            dpi=180,
            # framestyle=:box,
        )
    end
    begin #guides
        default(
            grid=:true,
            gridalpha=.3,
            minorgrid=:true,
            minorgridalpha=.0,
        )
    end
    begin #legend
        default(
            legend=:outertop,
            legendtitlefonthalign=:hcenter,
            legend_font_halign=:hcenter,
            # legend_columns=3,
        )
    end
    begin #fontsizes
        fs_base = style[:fontsizes][:fs_plot_body][:value]
        default(
            plot_titlefontsize=fs_base+4,
            titlefontsize=fs_base+2,
            guidefontsize=fs_base-2,
            tickfontsize=fs_base-4,
            colorbar_titlefontsize=fs_base-2,
            legendtitlefontsize=fs_base-6,
            legendfontsize=fs_base-6,
        )
    end
    begin #series defaults
        default(
            linewidth=2,
            markersize=4,
            markerstrokewidth=0,
            ls=:solid,
            markershape=:none,
        )
    end

    begin #colors
        default(
            bg=style[:colors][:c_bg][theme],
            bginside=style[:colors][:c_bg][theme],
            fg=style[:colors][:c_body_text][theme],
            fgtext=style[:colors][:c_body_text][theme],
            fgguide=style[:colors][:c_body_text][theme],
            legendfontcolor=style[:colors][:c_body_text][theme],
            legendtitlefontcolor=style[:colors][:c_body_text][theme],
            background_color_legend=nothing,
            foreground_color_legend=nothing,
            titlefontcolor=style[:colors][:c_body_text][theme],
        )
        default(
            color_palette=colorway,     #force cycling of these colors
            # color_palette=cgrad_lcs,    #keep sampling unique colors trying to spread them out
            # cmap=cgrad_lcs,             #NOTE: also overrides `color_palette`!!
        )
    end

    return colorway, ls, markers, cgrad_lcs, hatches
end

"""
    function fink(;
        theme::Symbol=:dark, cycle::Symbol=:cycle,
        )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}

applies style of the [FINK collaboration](https://fink-broker.org) to `Plots.jl` in the current session

- derived from [`tre`](@ref)

# Arguments
- `theme`
    - the theme to use
    - options are
        - `:dark`
        - `:light`
- `cycle`
    - mode to use for cycling through linestyles, markers, hatches, etc.
    - options are
        - `:cycle`
            - will cycle through the linestyles
            - every line consecutive line, marker, hatch, etc. will have a unique style
        - `:batch`
            - will batch similar linestyles together
            - consecutive lines, markes, hatches, etc. will have the same style

See also
- [`tre`](@ref)

## Returns
- `colorway`
    - color palette used to cycle through when plotting
- `ls`
    - linestyles used to cycle through when plotting
- `markers`
    - markers used to cycle through when plotting
- `cmap`
    - colormap used in the style
- `hatches`
    - hatches used to cycle through when plotting

# Extended help

## Dependencies
- [`Plots`](@ref)
- [`PlotUtils`](@ref)
"""
function fink(;
    theme::Symbol=:dark, cycle::Symbol=:cycle,
    )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}

    #override some colors
    fink_colors = [
        "#15284F",
        "#3C8DFF",
        "#D5D5D3",
        "#F5622E",
    ]
    if theme == :dark
        cmap = cgrad(
            fink_colors[[1,3,4]],
            [0.0, 0.5, 1.0];
            rev=true,
        )
        colorway = reverse(fink_colors[2:end])
    elseif theme == :light
        cmap = cgrad(
            fink_colors[[1,3,4]],
            [0.0, 0.5, 1.0];
            rev=false,
        )
        colorway = fink_colors
    else
        throw("invalid `theme` ($(theme))")
    end

    colorway, ls, markers, cmap, hatches = tre(;
        theme=theme, cycle=cycle,
        colorway_override=colorway, cmap_override=cmap
    )

    return colorway, ls, markers, cmap, hatches
end

"""
    function lust(;
        theme::Symbol=:dark, cycle::Symbol=:cycle,
        )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}

applies the LuSt style to `Plots.jl` in the current session

- derived from [`tre`](@ref)

# Arguments
- `theme`
    - the theme to use
    - options are
        - `:dark`
        - `:light`
- `cycle`
    - mode to use for cycling through linestyles, markers, hatches, etc.
    - options are
        - `:cycle`
            - will cycle through the linestyles
            - every line consecutive line, marker, hatch, etc. will have a unique style
        - `:batch`
            - will batch similar linestyles together
            - consecutive lines, markes, hatches, etc. will have the same style

See also
- [`tre`](@ref)

## Returns
- `colorway`
    - color palette used to cycle through when plotting
- `ls`
    - linestyles used to cycle through when plotting
- `markers`
    - markers used to cycle through when plotting
- `cmap`
    - colormap used in the style
- `hatches`
    - hatches used to cycle through when plotting

# Extended help

## Dependencies
- [`Plots`](@ref)
- [`PlotUtils`](@ref)
"""
function lust(;
    theme::Symbol=:dark, cycle::Symbol=:cycle,
    )::Tuple{Vector,Vector{Symbol},Vector{Symbol},PlotUtils.ContinuousColorGradient,Vector{Symbol}}

    #override some colors
    if theme == :dark
        cmap        = cgrad(:coolwarm; rev=true)
        colorway    = ["#A10000", "#51BFFF", "#FF7B00", "#B500BB", "#CFC100", "#009E69"]
    elseif theme == :light
        cmap        = cgrad(:coolwarm; rev=false)
        colorway    = ["#A10000", "#51BFFF", "#FF7B00", "#B500BB", "#CFC100", "#009E69"]
    else
        throw("invalid `theme` ($(theme))")
    end

    colorway, ls, markers, cmap, hatches = tre(;
        theme=theme, cycle=cycle,
        colorway_override=colorway, cmap_override=cmap
    )

    return colorway, ls, markers, cmap, hatches
end


"""

    exposes custom themes to `Plots.jl` interface
"""
function include_themes()
    PlotThemes.add_theme(:tre_dark, _tre_dark)
    PlotThemes.add_theme(:tre_light, _tre_light)
end

#%%themes
begin #specify layout, sizes, ...
    layout_specs = Dict([
        #fontsizes
        :plot_titlefontsize     => 20,
        :titlefontsize          => 16,
        :guidefontsize          => 14,
        :tickfontsize           => 12,
        :colorbar_titlefontsize => 14,
        :legendtitlefontsize    => 10,
        :legendfontsize         => 10,
        # :legendtitlefonthalign  =>:right,
        #frame layout
        :size                   => (900,500),
        :top_margin             => 6Plots.mm,
        :bottom_margin          => 6Plots.mm,
        :left_margin            => 6Plots.mm,
        :right_margin           => 6Plots.mm,
        :dpi                    => 180,
        # :framestyle             => :box,
        #grid lyout
        :grid                   => :true,
        :gridalpha              => .3,
        :minorgrid              => :true,
        :minorgridalpha         => .0,
        #marker and line defaults
        # :marker                 => :auto,
        :linewidth              => 2,
        :markersize             => 4,
        :markerstrokewidth      => 0,
        :ls                     => :solid,
    ])

    #options for monochrome plots
    """
        - has presets for `ncolors_mono*nlinestyles_mono` lines
        - has presets for `ncolors_mono*nmarkers_mono` markers
        - `mono_ls` contains `ncolors_mono*nlinestyles_mono` linestyles.
            - Each ls gets repeated `ncolors_mono` times
            - Then the next color is applied
        - `mono_markers` contains `ncolors_mono*nmarkers_mono` markers.
            - Each marker gets repeated `ncolors_mono` times
            - Then the next color is applied
        - The idea here is that each `mono_ls`/`mono_markers` will be plotted in each color, then plot the proceed to the next  in the next `mono_ls`/`mono_markers` etc.
            - This way, the lines/scatters will always be distinguishable
    """
    ncolors_mono        = 3

    mono_colors_base    = collect(cgrad(:grays, ncolors_mono+1, categorical=true, rev=false))
    mono_ls_base        = [:solid :dash :dot :dashdot :dashdotdot]              #linestyles to cycle through when plotting
    mono_markers_base   = [:circle :utriangle :dtriangle :diamond :cross]       #markers to cycle through

    nlinestyles_mono    = length(mono_ls_base)           #number of defined linestyles
    nmarkers_mono       = length(mono_markers_base)      #number of defined linestyles

    const mono_colors_light = reshape(RGB.(reshape(repeat(mono_colors_base[1:end-1], 1,nlinestyles_mono),:)), 1, :)
    const mono_colors_dark  = reshape(RGB.(reshape(repeat(mono_colors_base[2:end], 1,nlinestyles_mono),:)), 1, :)
    const mono_ls           = hcat(permutedims(reshape(repeat(mono_ls_base, 1, ncolors_mono), :, ncolors_mono), (2,1))...)
    const mono_markers      = hcat(permutedims(reshape(repeat(mono_markers_base, 1, ncolors_mono), :, ncolors_mono), (2,1))...)

end

begin #tre_dark
    #add changes to `layout_specs`
    layout_specs_tre_dark = copy(layout_specs)

    const tre_dark_palette = [colorant"rgb(161,0,0)", mono_colors_dark[end:-1:1]...]

    const tre_dark_bg = colorant"#000000"

    color_scheme = Dict([
        :bg                     => tre_dark_bg,
        :bginside               => colorant"#000000",
        :fg                     => colorant"rgba(100%,100%,100%,1)",
        :fgtext                 => colorant"rgba(100%,100%,100%,1)",
        :fgguide                => colorant"rgba(100%,100%,100%,1)",
        :fglegend               => colorant"rgba(100%,100%,100%,1)",
        :legendfontcolor        => colorant"rgba(100%,100%,100%,1)",
        :legendtitlefontcolor   => colorant"rgba(100%,100%,100%,1)",
        :legendbackgroundcolor  => colorant"rgba(0%,  0%,  0%,  0.07)",
        :titlefontcolor         => colorant"rgba(100%,100%,100%,1)",
        :palette                => PlotThemes.expand_palette(tre_dark_bg, tre_dark_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => :grays,
    ])

    const _tre_dark = PlotTheme(merge(color_scheme, layout_specs_tre_dark))
end

begin #tre_light
    #add changes to `layout_specs`
    layout_specs_tre_light = copy(layout_specs)
    # layout_specs_tre_light[:ls] = mono_ls
    # layout_specs_tre_light[:ls] = :auto
    # layout_specs_tre_light[:markershape] = markershape_mono

    const tre_light_palette = [colorant"rgb(161,0,0)", mono_colors_light[1:end]...]


    const tre_light_bg = colorant"#FFFFFF"

    color_scheme = Dict([
        :bg                     => tre_light_bg,
        :bginside               => colorant"#FFFFFF",
        :fg                     => colorant"rgba(0,0,0,1)",
        :fgtext                 => colorant"rgba(0,0,0,1)",
        :fgguide                => colorant"rgba(0,0,0,1)",
        :fglegend               => colorant"rgba(0,0,0,1)",
        :legendfontcolor        => colorant"rgba(0,0,0,1)",
        :legendtitlefontcolor   => colorant"rgba(0,0,0,1)",
        :legendbackgroundcolor  => colorant"rgba(0,0,0,0.07)",
        :titlefontcolor         => colorant"rgba(0,0,0,1)",
        :palette                => PlotThemes.expand_palette(tre_light_bg, tre_light_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => cgrad(:grays, rev=true),
    ])

    const _tre_light = PlotTheme(merge(color_scheme, layout_specs_tre_light))
end


end #module

