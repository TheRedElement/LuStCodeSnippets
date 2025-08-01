
#%%imports
using Plots

using LuStCodeSnippets_jl: PlotStyles

PlotStyles.include_themes()
gr()

theme(:lust_dark)
theme(:lust_light)
theme(:lust_dark_mono)
theme(:lust_light_mono)
theme(:tre_dark)
# theme(:tre_light)

#%%definitions

#%%demos
begin
    #lineplot
    p1 = plot((1:9) .+ (1:10)', xlabel="X", ylabel="Y", seriestype=:line, ls=PlotStyles.mono_ls, alpha=1)#, linecolor=PlotStyles.mono_colors)
    vline!(p1, [2,4,6]; color=1, alpha=.2, label="")
    plot!(p1, legendtitle="LEGTIT")

    #heatmap
    hm = heatmap(randn(50,50), xlabel="X", ylabel="Y", colorbar_title="Cbar")

    #3d surface
    p2 = surface(
        1:5, 1:5, repeat(1:5, 1,5),
        colorbar_title="Cbar", 
    )

    #scatter
    s1 = plot(randn(15), randn(15), zcolor=log.(rand(15) .+ 1), seriestype=:scatter, cmap=:coolwarm, colorbar_title="test")
    plot!(s1, randn(15,6), randn(15,6), seriestype=:scatter, m=PlotStyles.mono_markers)

    #histogram
    x = randn(300)
    hg = histogram(x; fillstyle=:x, linestyle=:dash, color=1, linecolor=1)

    #combine
    plot(p1, hm, p2, s1, hg;
        layout=@layout[ [a ; b] [c ; d] ; e],
        title="TITLE", plot_title="Suptitle",
        size=(1200,1200)
    )
end