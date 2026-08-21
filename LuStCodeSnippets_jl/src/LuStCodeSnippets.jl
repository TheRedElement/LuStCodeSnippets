"""
LuStCodeSnippets package
"""

module LuStCodeSnippets

#%%imports
using Dates

#metadata
const __modulename__ = "LuStCodeSnippets"
const __version__ = "0.1.0"
const __author__ = "Lukas Steinwender"
const __author_email__ = ""
const __maintainer__ = "Lukas Steinwender"
const __maintainer_email__ = ""
const __url__ = "https://github.com/TheRedElement/LuStCodeSnippets"
const __credits__ = ""
const __last_changed__ = string(Dates.today())


begin #fundamental submodules
    include("./LcsBase/LcsBase.jl")

    #add submodules (make visible to parent module)
    using .LcsBase

    #reexport submodules (make accesible to user)
    export LcsBase
end

begin #submodules without intradependencies
    #add submodules (make visible to parent module)
    include("./Colorings.jl")
    include("./DataFramesConvenience.jl")

    #load submodules (make visible to parent module)
    using .Colorings
    using .DataFramesConvenience

    #reexport submodules (make accesible to user)
    export Colorings
    export DataFramesConvenience
end

begin #submodules only dependent on `LcsBase`
    #add submodules (make visible to parent module)
    include("./PlotsStyle.jl")

    #load submodules (make visible to parent module)
    using .PlotsStyle

    #reexport submodules (make accesible to user)
    export PlotsStyle
end

begin #submodules relying on other modules
end

end #module
