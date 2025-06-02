
#%%imports
using Plots
# using NaNStatistics

using astroLuStjl.Styles.FormattingUtils
using astroLuStjl.Styles.PlotStyle
using astroLuStjl.Visualization.PlotTypes

gr()
# plotlyjs()
# pgfplotsx()

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
    p1 = plot((1:9) .+ (1:10)', xlabel="X", ylabel="Y", seriestype=:line, ls=PlotStyleLuSt.mono_ls, alpha=1)#, linecolor=PlotStyleLuSt.mono_colors)
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
    plot!(s1, randn(15,6), randn(15,6), seriestype=:scatter, m=PlotStyleLuSt.mono_markers)#, size=(2000,1500))

    #histogram
    x = randn(300)
    hg = histogram(x; fillstyle=:x, linestyle=:dash, color=1, linecolor=1)

    #custom hatched histogram
    hhg = PlotTypes.hatched_histogram(
        x;
        k=-5, offset=2, npoints=50, ls=:dash,
        normalize=:false, fillalpha=0, fillcolor=1
    )
    PlotTypes.hatched_histogram!(hhg, x; k=5, offset=2, ls=:dash)

    #combine
    plot(p1, hm, p2, s1, hg, hhg;
        layout=@layout[ [a ; b] [c ; d] ; [e{.3h} f{.3h}]],
        title="TITLE", plot_title="Suptitle",
        size=(1200,1200)
    )
end