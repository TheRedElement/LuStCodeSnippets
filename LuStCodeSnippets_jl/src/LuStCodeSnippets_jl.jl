"""
LuStCodeSnippets package
"""

module LuStCodeSnippets_jl

#%%imports
using Dates

#metadata
const __modulename__ = "LuStCodeSnippets_jl" 
const __version__ = "0.1.0"
const __author__ = "Lukas Steinwender"
const __author_email__ = ""
const __maintainer__ = "Lukas Steinwender"
const __maintainer_email__ = ""
const __url__ = "https://github.com/TheRedElement/code_snippets"
const __credits__ = ""
const __last_changed__ = string(Dates.today())

#add submodules (make visible to parent module)
include("./Colorings.jl")
include("./DataFramesConvenience.jl")
include("./PlotStyles.jl")

#load submodules (make visible to parent module)
using .Colorings
using .DataFramesConvenience
using .PlotStyles

#reexport submodules (make accesible to user)
export Colorings
export DataFramesConvenience
export PlotStyles

end #module