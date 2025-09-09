

"""
    - module to include custom plotting styles
    - to use the styles simply call the following

    Constants
    ---------
        - `mono_ls`
            - `Vector{Symbol}`
            - linestyles used in monochromatic styles
            - contains `ncolors_mono*nlinestyles_mono` linestyles.
                - each ls gets repeated `ncolors_mono` times
                - then the next color and ls is applied
                - this way, the lines will always be distinguishable
        - `mono_markers`
            - `Vector{Symbol}`
            - markershapes used in monochromatic styles        
            - contains `ncolors_mono*nmarkers_mono` markers.
            - each marker gets repeated `ncolors_mono` times
            - then the next color and marker is applied            
            - this way, the markers will always be distinguishable
        - `mono_colors`
            - `Vector{RGB}`
            - colors used in monochromatic styles
            
    Structs
    -------

    Functions
    ---------
        - `include_themes()`

    Dependencies
    ------------
        - `Colors`
        - `FixedPointNumbers`
        - `Plots`
        - `PlotThemes`
        - `Revise`

    Comments
    --------
        - for the following themes `[:lust_light_mono,:lust_dark_mono,:tre_dark,:tre_light]`
            - make sure to call `ls=mono_ls[i]` in line plots
            - `i` is the index of the plotted series in order
        - make sure to call `marker=markers_mono[i]` in scatter plots
            - `i` is the index of the plotted series in order
        - resources
            - https://docs.juliaplots.org/latest/api/
            - https://docs.juliaplots.org/latest/generated/supported/
        - always use `clorant"rgba(...)"` when specifying new style
            - other specifications are not compatible across all backends!

    Examples
    --------
        - see [PlotStyleLuSt_demo.jl](./../demos/styles/PlotStyleLuSt_demo.jl)
        - loading the styles
```julia
    using Plots
    using LuStCodeSnippets_jl: PlotStyleLuSt
    PlotStyleLuSt.include_themes()

    #choose your theme
    # theme(:lust_dark)
    # theme(:lust_light)
    # theme(:lust_light_mono)
    # theme(:lust_dark_mono)
    theme(:tre_dark)
    # theme(:tre_light)
```    
```julia

```

"""
module PlotStyles

#%%imports
using Colors
using FixedPointNumbers
using Plots
using PlotThemes

#import for extending

#intradependencies

#%%exports
export mono_ls
export mono_markers
export mono_colors
export include_themes


#%%definitions

#######################################
#helper functions
"""
    - function to interleave two vectors

    Parameters
    ----------
        - `x`
            - `Vector`
            - vector the elements of which will be inserted at odd indices
        - `y`
            - `Vector`
            - vector the elements of which will be inserted at even indices

    Raises
    ------
        - `AssertionError`
            - if legnths of `x` and `y` do not match

    Returns
    -------
        - `out`
            - `Vector`
            - vector of the interleaved entries of `x` and `y`
            - has length `length(x) + length(y)`

    Dependencies
    ------------
"""
function interleave(
    x::Vector, y::Vector
    )::Vector

    @assert length(x) == length(y) "`x` and `y` have to have the same length but are `$(length(x))` and `$(length(y))`"

    n = length(x) + length(y)
    out = Vector{Any}(undef, n)
    out[1:2:end] .= x
    out[2:2:end] .= y

    return out

end

#######################################
#custom styles
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

begin #lust_dark
    # const tre_dark_palette = [
    #     colorant"rgba(161,  0,0,1)", #red
    #     colorant"rgba(161,100,0,1)", #orange
    #     colorant"rgba(161,161,0,1)", #yellow
    # ]

    const lust_dark_palette = convert.(RGB{N0f8}, range(
        HSL(colorant"red"),
        HSL(colorant"purple"),
        length=9,
    ))

    const lust_dark_bg = colorant"#000000"

    color_scheme = Dict([
        :bg                     => lust_dark_bg,
        :bginside               => colorant"#000000",
        :fg                     => colorant"rgba(100%,100%,100%,1)",
        :fgtext                 => colorant"rgba(100%,100%,100%,1)",
        :fgguide                => colorant"rgba(100%,100%,100%,1)",
        :fglegend               => colorant"rgba(100%,100%,100%,1)",
        :legendfontcolor        => colorant"rgba(100%,100%,100%,1)",
        :legendtitlefontcolor   => colorant"rgba(100%,100%,100%,1)",
        :legendbackgroundcolor  => colorant"rgba( 0%, 0%, 0%,0.07)",
        :titlefontcolor         => colorant"rgba(100%,100%,100%,1)",
        :palette                => PlotThemes.expand_palette(lust_dark_bg, lust_dark_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => :fire,
    ])

    #define layout
    const _lust_dark = PlotTheme(merge(color_scheme, layout_specs))
end

begin #lust_light

    const lust_light_palette = convert.(RGB{N0f8}, range(
        HSL(colorant"red"),
        HSL(colorant"purple"),
        length=9,
    ))

    const lust_light_bg = colorant"#FFFFFF"

    color_scheme = Dict([
        :bg                     => lust_light_bg,
        :bginside               => colorant"#FFFFFF",
        :fg                     => colorant"rgba(0,0,0,1)",
        :fgtext                 => colorant"rgba(0,0,0,1)",
        :fgguide                => colorant"rgba(0,0,0,1)",
        :fglegend               => colorant"rgba(0,0,0,1)",
        :legendfontcolor        => colorant"rgba(0,0,0,1)",
        :legendtitlefontcolor   => colorant"rgba(0,0,0,1)",
        :legendbackgroundcolor  => colorant"rgba(0,0,0,0.07)",
        :fg_legend              => colorant"rgba(0,0,0,1)",
        :titlefontcolor         => colorant"rgba(0,0,0,1)",
        :palette                => PlotThemes.expand_palette(lust_light_bg, lust_light_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => :fire,
    ])

    const _lust_light = PlotTheme(merge(color_scheme, layout_specs))
end

begin #lust_dark_mono (monochromatic)

    # # const lust_dark_mono_palette = palette(:grayC10, 7, rev=true)[1:end-1]
    # const lust_dark_mono_palette = distinguishable_colors(
    #     11, [colorant"black", colorant"white"],
    #     dropseed=false,
    #     # lchoices=[30],
    #     cchoices=[0],
    #     # hchoices=[290]
    # )[3:end]

    #add changes to `layout_specs`
    layout_specs_lust_dark_mono = copy(layout_specs)
    # layout_specs_lust_dark_mono[:ls] = mono_ls
    # layout_specs_lust_dark_mono[:ls] = :auto
    # layout_specs_lust_dark_mono[:markershape] = markershape_mono
    
    const lust_dark_mono_palette = mono_colors_dark[end:-1:1]


    color_scheme = Dict([
        :bg                     => lust_dark_bg,
        :bginside               => colorant"#000000",
        :fg                     => colorant"rgba(100%,100%,100%,1)",
        :fgtext                 => colorant"rgba(100%,100%,100%,1)",
        :fgguide                => colorant"rgba(100%,100%,100%,1)",
        :fglegend               => colorant"rgba(100%,100%,100%,1)",
        :legendfontcolor        => colorant"rgba(100%,100%,100%,1)",
        :legendtitlefontcolor   => colorant"rgba(100%,100%,100%,1)",
        :legendbackgroundcolor  => colorant"rgba(0%,  0%, 0%,0.07)",
        :titlefontcolor         => colorant"rgba(100%,100%,100%,1)",
        :palette                => PlotThemes.expand_palette(lust_dark_bg, lust_dark_mono_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => :grays,
    ])

    const _lust_dark_mono = PlotTheme(merge(color_scheme, layout_specs_lust_dark_mono))
end

begin #lust_light_mono (monochromatic)

    #add changes to `layout_specs`
    layout_specs_lust_light_mono = copy(layout_specs)
    # layout_specs_lust_light_mono[:ls] = mono_ls
    # layout_specs_lust_light_mono[:ls] = :auto
    # layout_specs_lust_light_mono[:markershape] = markershape_mono
    
    const lust_light_mono_palette = mono_colors_light[1:end]

    color_scheme = Dict([
        :bg                     => lust_light_bg,
        :bginside               => colorant"#FFFFFF",
        :fg                     => colorant"rgba(0,0,0,1)",
        :fgtext                 => colorant"rgba(0,0,0,1)",
        :fgguide                => colorant"rgba(0,0,0,1)",
        :fglegend               => colorant"rgba(0,0,0,1)",
        :legendfontcolor        => colorant"rgba(0,0,0,1)",
        :legendtitlefontcolor   => colorant"rgba(0,0,0,1)",
        :legendbackgroundcolor  => colorant"rgba(0,0,0,0.07)",
        :titlefontcolor         => colorant"rgba(0,0,0,1)",
        :palette                => PlotThemes.expand_palette(lust_light_bg, lust_light_mono_palette; lchoices=[57], cchoices=[100]),
        :colorgradient          => cgrad(:grays, rev=true),
    ])

    const _lust_light_mono = PlotTheme(merge(color_scheme, layout_specs_lust_light_mono))
end

begin #tre_dark
    
    #add changes to `layout_specs`
    layout_specs_tre_dark = copy(layout_specs)
    # layout_specs_tre_dark[:ls] = mono_ls
    # layout_specs_tre_dark[:ls] = :auto
    # layout_specs_tre_dark[:markershape] = markershape_mono
    
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


#######################################
#include custom styles
"""
    - function to make custom themes visible to global scope

    Parameters
    ----------

    Raises
    ------

    Returns
    -------

    Comments
    --------
"""
function include_themes()
    PlotThemes.add_theme(:lust_dark, _lust_dark)
    PlotThemes.add_theme(:lust_light, _lust_light)
    PlotThemes.add_theme(:lust_light_mono, _lust_light_mono)
    PlotThemes.add_theme(:lust_dark_mono, _lust_dark_mono)
    PlotThemes.add_theme(:tre_dark, _tre_dark)
    PlotThemes.add_theme(:tre_light, _tre_light)
end

end #module