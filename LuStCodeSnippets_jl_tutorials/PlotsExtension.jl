using Base: return_types
"""
tutorials for [`LuStCodeSnippets.PlotsExtension`](@ref)
"""

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

pgfplotsx()
# gr()

#%%constants
GFX_PATH::String = joinpath(@__DIR__, "../gfx/")

#%%definitions
function save_latex()

    #create some testplot
    colorway, ls, markers, cmap, hatches = PlotsStyle.tre(theme=:light, cycle=:batch)
    p = PlotsExtension.testplot(;
        colorway=colorway,
        ls=ls, markers=markers,
        cmap=cmap,
        hatches=hatches,
    )

    #save
    PlotsExtension.save_latex(p, joinpath(GFX_PATH, "PlotsExtension_save_latex.tikz");
        thickness_scaling=2.0,
    )

    return nothing
end

#%%main
function main()
    plots = []

    if backend_name == :pgfplotsx
        save_latex()
        println(backend_name())
    end

    for (idx, p) in enumerate(plots[1:end])
        savefig(p, joinpath(GFX_PATH, "PlotsExtension_$(idx).svg"))
        display(p)
    end
end

main()
