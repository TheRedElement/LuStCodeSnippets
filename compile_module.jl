#%%imports
using Pkg
using TOML
using UUIDs

#add missing packages
# Pkg.add("Logging")

#module
include("./LuStCodeSnippets_jl/src/LuStCodeSnippets.jl")
using .LuStCodeSnippets

#%%definitions
"""
    build_project_toml(
        project_toml::String="./Project.toml",
        )

builds the project into an installable module

# Arguments
- `project_toml`
    - path to `Project.toml` file of the module


# Extended help

## Dependencies
- [`Pkg`](@ref)
- [`TOML`](@ref)
- [`UUIDs`](@ref)

"""
function build_project_toml(
    project_toml::String="./Project.toml",
    )

    #build first template (only contains dependencies)
    Pkg.activate(joinpath(@__DIR__, "./LuStCodeSnippets"))      #activate project env
    Pkg.resolve()                                               #ensure dependencies are up to date
    Pkg.status()                                                #list dependencies

    #read file
    toml = TOML.parsefile(project_toml)

    #add additional metadata
    toml["name"]            = LuStCodeSnippets.__modulename__
    toml["version"]         = LuStCodeSnippets.__version__
    toml["description"]     = "repository of some useful code snippets in various programming languages."
    toml["author"]          = LuStCodeSnippets.__author__
    toml["author_email"]    = LuStCodeSnippets.__author_email__
    toml["maintainer"]      = LuStCodeSnippets.__maintainer__
    toml["maintainer_email"]= LuStCodeSnippets.__maintainer_email__
    toml["url"]             = LuStCodeSnippets.__url__
    toml["credits"]         = LuStCodeSnippets.__credits__
    toml["last_changed"]    = LuStCodeSnippets.__last_changed__
    toml["uuid"]            = string(UUIDs.uuid4())

    println(toml)

    #add `[compat]` section
    toml["compat"] = Dict(
        "julia" => string(VERSION)              #julia version
    )

    # Write back to `Project.toml`
    open(project_toml, "w") do io
        TOML.print(io, toml)
    end

end

#%%main
build_project_toml(
    "./LuStCodeSnippets_jl/Project.toml"
)
