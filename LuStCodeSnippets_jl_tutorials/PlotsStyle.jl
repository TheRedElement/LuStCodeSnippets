
#%%imports
using Pkg
using Logging
using Plots
using Revise

using LuStCodeSnippets: PlotsStyle

PlotsStyle.include_themes()
gr()


#%%definitions
function testplot()::Plots.Plot
    #lineplot
    p1 = plot((1:9) .+ (1:10)', xlabel="X", ylabel="Y", seriestype=:line, ls=PlotsStyle.mono_ls, alpha=1)#, linecolor=PlotsStyle.mono_colors)
    vline!(p1, [2,4,6]; color=1, alpha=.2, label="")
    plot!(p1, legendtitle="LEGTIT", legend_columns=5)

    #heatmap
    hm = heatmap(randn(50,50), xlabel="X", ylabel="Y", colorbar_title="Cbar")

    #3d surface
    p2 = surface(
        1:5, 1:5, repeat(1:5, 1,5),
        colorbar_title="Cbar",
    )

    #scatter
    s1 = plot(randn(15), randn(15), zcolor=log.(rand(15) .+ 1), seriestype=:scatter, cmap=:coolwarm, colorbar_title="test")
    plot!(s1, randn(15,6), randn(15,6), seriestype=:scatter, m=PlotsStyle.mono_markers)

    #histogram
    x = randn(300)
    hg = histogram(x; fillstyle=:x, linestyle=:dash, color=1, linecolor=1)

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

    begin   #function based
        PlotsStyle.tre()
        push!(plots, testplot())
    end


    begin   #theme based
        # theme(:tre_dark)
        # push!(plots, testplot())
        # theme(:tre_light)
        # push!(plots, testplot())
    end

    for (idx, p) in enumerate(plots)
        display(p)
        savefig(p, joinpath(@__DIR__, "../gfx/temp_PlotsJl_$(idx).svg"))
    end
end

main()
