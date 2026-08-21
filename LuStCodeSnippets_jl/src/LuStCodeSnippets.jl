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

#add submodules (make visible to parent module)
include("./Colorings.jl")
include("./DataFramesConvenience.jl")
include("./PlotsStyle.jl")

#load submodules (make visible to parent module)
using .Colorings
using .DataFramesConvenience
using .PlotsStyle

#reexport submodules (make accesible to user)
export Colorings
export DataFramesConvenience
export PlotsStyle

end #module
