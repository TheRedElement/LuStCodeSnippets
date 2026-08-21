
module Loaders

#%%imports

#import for extending

#intradependencies

#%%exports
export get_datapath

#%%constants

#%%definitions
"""
    get_datapath()::Union{String,Nothing}

returns path to module-internal data-directory
"""
function get_datapath()::Union{String,Nothing}
    if isnothing(pkgdir(parentmodule(@__MODULE__)))
        @warn "`pkgdir(parentmodule(@__MODULE__))` is `nothing`... setting `data_dir` to `nothing`"
        return nothing
    else
        data_dir::String = joinpath(pkgdir(parentmodule(@__MODULE__)), "_data")
    end
    return data_dir
end

end #module
