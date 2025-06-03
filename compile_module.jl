#%%imports
using Pkg
using TOML
using UUIDs

#module
include("./LuStCodeSnippets_jl/src/LuStCodeSnippets_jl.jl")
using .LuStCodeSnippets_jl

#%%definitions
"""
    - function to build the project into an installable module

    Parameters
    ----------
        - `project_toml`
            - `String`, optional
            - path to `Project.toml` file of the module
            - the default is `./Project.toml`

    Raises
    ------

    Returns
    -------

    Dependencies
    ------------
        - `Pkg`
        - `TOML`
        - `UUIDs`

    Comments
    --------

"""
function build_project_toml(
    project_toml::String="./Project.toml",
    )

    #build first template (only contains dependencies)
    Pkg.activate(joinpath(@__DIR__, "./LuStCodeSnippets_jl"))   #activate project env
    Pkg.resolve()                                               #ensure dependencies are up to date
    Pkg.status()                                                #list dependencies

    #read file
    toml = TOML.parsefile(project_toml)
    
    #add additional metadata
    toml["name"]            = LuStCodeSnippets_jl.__modulename__
    toml["version"]         = LuStCodeSnippets_jl.__version__
    toml["description"]     = "repository of some useful code snippets in various programming languages."
    toml["author"]          = LuStCodeSnippets_jl.__author__
    toml["author_email"]    = LuStCodeSnippets_jl.__author_email__
    toml["maintainer"]      = LuStCodeSnippets_jl.__maintainer__
    toml["maintainer_email"]= LuStCodeSnippets_jl.__maintainer_email__
    toml["url"]             = LuStCodeSnippets_jl.__url__
    toml["credits"]         = LuStCodeSnippets_jl.__credits__
    toml["last_changed"]    = LuStCodeSnippets_jl.__last_changed__
    toml["uuid"]            = string(UUIDs.uuid4())

    println(toml)

    #add `[compat]` section
    toml["compat"] = Dict(
        "julia" => string(VERSION)              #juia version
    )

    # Write back to `Project.toml`
    open(project_toml, "w") do io
        TOML.print(io, toml)
    end

end


#%%control

#%%main
build_project_toml(
    "./LuStCodeSnippets_jl/Project.toml"
)