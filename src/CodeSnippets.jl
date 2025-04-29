"""
CodeSnippets package
"""

module CodeSnippets

#%%imports
using Dates

#metadata
const __modulename__ = "CodeSnippets" 
const __version__ = "0.1.0"
const __author__ = "Lukas Steinwender"
const __author_email__ = ""
const __maintainer__ = "Lukas Steinwender"
const __maintainer_email__ = ""
const __url__ = "https://github.com/TheRedElement/code_snippets"
const __credits__ = ""
const __last_changed__ = string(Dates.today())

#add submodules (make visible to parent module)
include("../src_jl/Colorings.jl")

#load submodules (make visible to parent module)
using .Colorings

#reexport submodules (make accesible to user)
export Colorings

end #modle