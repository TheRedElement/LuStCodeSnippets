

"""

    defines styles for `Plots.jl`


    Functions
        - [`include_themes`](@ref) -- exposes custom themes to `Plots.jl` interface

    Comments
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
module PlotsStyle

#%%imports
using JSON

using Colors
using FixedPointNumbers
using Plots
using PlotThemes

#import for extending

#intradependencies

#%%exports
export tre

export mono_ls
export mono_markers
export mono_colors
export include_themes

#%%constants
const DATA_DIR::String = joinpath(pkgdir(parentmodule(@__MODULE__)), "_data")

#%%definitions
function tre(;
    theme::Symbol=:dark, cycle::Symbol=:cycle,
    colorway_override=false, cmap_override=false,
    )


    #load style from json
    style = JSON.parsefile(joinpath(DATA_DIR, "tre_PlotsJl.json"))

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


"""

    exposes custom themes to `Plots.jl` interface
"""
function include_themes()
    PlotThemes.add_theme(:tre_dark, _tre_dark)
    PlotThemes.add_theme(:tre_light, _tre_light)
end

end #module

