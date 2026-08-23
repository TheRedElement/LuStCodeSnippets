
#%%imports
using Pkg
using Logging
using Plots
using Revise

Pkg.resolve()
# Pkg.rm("LuStCodeSnippets")
# Pkg.develop(path="./LuStCodeSnippets_jl/")

using LuStCodeSnippets: PlotsStyle
using LuStCodeSnippets: PlotsExtension

PlotsStyle.include_themes()
gr()
pgfplotsx()

#%%constants
GFX_PATH::String = joinpath(@__DIR__, "../gfx/")

#%%definitions

#%%main
function main()
    plots = []

    begin   #function based (preferred)
        #tre (base style)
        colorway, ls, markers, cmap, hatches = PlotsStyle.tre()
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
        colorway, ls, markers, cmap, hatches = PlotsStyle.tre(theme=:light, cycle=:batch)
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))

        #fink
        colorway, ls, markers, cmap, hatches = PlotsStyle.fink(
            theme=:dark, cycle=:cycle,
        )
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
        colorway, ls, markers, cmap, hatches = PlotsStyle.fink(
            theme=:light, cycle=:batch,
        )
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))

        #lust
        colorway, ls, markers, cmap, hatches = PlotsStyle.lust(
            theme=:dark, cycle=:cycle,
        )
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
        colorway, ls, markers, cmap, hatches = PlotsStyle.lust(
            theme=:light, cycle=:batch,
        )
        push!(plots, PlotsExtension.testplot(;
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
        push!(plots, PlotsExtension.testplot(;
            colorway=colorway,
            ls=ls, markers=markers,
            cmap=cmap,
            hatches=hatches,
        ))
    end

    begin   #theme based
        theme(:tre_dark)
        push!(plots, PlotsExtension.testplot())
        theme(:tre_light)
        push!(plots, PlotsExtension.testplot())
    end

    for (idx, p) in enumerate(plots[1:end])
        if backend_name() == :pgfplotsx
            PlotsExtension.save_latex(plots[idx], joinpath(GFX_PATH, "temp_PlotsJl_$(idx).tikz");
                thickness_scaling=2.0,
            )
        else
            savefig(p, joinpath(GFX_PATH, "temp_PlotsJl_$(idx).svg"))
            display(p)
        end
    end
end

main()
