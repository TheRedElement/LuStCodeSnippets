
#%%imports
using Pkg
using Logging
using Plots
using Revise

# Pkg.remove("LuStCodeSnippets")
# Pkg.dev("./LuStCodeSnippets_jl")

using LuStCodeSnippets: PlotsStyle

PlotsStyle.include_themes()
gr()


#%%definitions
"""

creates a testplot for testing different styles/themes
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
        layout=@layout[ [a ; b] [c ; d] ; e],
        title="TITLE", plot_title="Suptitle",
        size=(1200,1200)
    )
    return p
end


#%%main
function main()
    plots = []

    begin   #function based (preferred)
        #tre (base style)
        colorway, ls, markers, cmap, hatches = PlotsStyle.tre()
        push!(plots, testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
        colorway, ls, markers, cmap, hatches = PlotsStyle.tre(theme=:light, cycle=:batch)
        push!(plots, testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))

        #lust
        colorway, ls, markers, cmap, hatches = PlotsStyle.lust(
            theme=:dark, cycle=:cycle,
        )
        push!(plots, testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
        colorway, ls, markers, cmap, hatches = PlotsStyle.lust(
            theme=:light, cycle=:batch,
        )
        push!(plots, testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))


        #quick customizations
        colorway, ls, markers, cmap, hatches = PlotsStyle.tre(
            theme=:dark, cycle=:cycle,
            colorway_override=["#f49bf4","#eaff74","#91fecb","#82aef6"],
            cmap_override=cgrad(:roma; rev=true),
            # cmap_override=:roma,
        )
        push!(plots, testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
    end


    begin   #theme based
        theme(:tre_dark)
        push!(plots, testplot())
        theme(:tre_light)
        push!(plots, testplot())
    end

    for (idx, p) in enumerate(plots)
        display(p)
        savefig(p, joinpath(@__DIR__, "../gfx/temp_PlotsJl_$(idx).svg"))
    end
end

main()
