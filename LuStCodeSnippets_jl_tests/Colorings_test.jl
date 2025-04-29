
#%%imports
using Colors
using Random

include(joinpath(@__DIR__, "../src_jl/Colorings.jl"))
using .Colorings

#%%tests
@testset "Colorings" begin
    @testset "colorcode" begin
        @test begin
            rng = Xoshiro(0)
            truth = [RGB(0.719956090909091, 0.19253427272727275, 0.5419935454545455), RGB(0.050383, 0.029803, 0.527975), RGB(0.940015, 0.975158, 0.131326), RGB(0.10736545454545456, 0.024194909090909093, 0.5519892121212121), RGB(0.9668503636363638, 0.5645567272727272, 0.2650150606060606)]
            x = collect(rand(rng, range(-5,5,101), 5))
            res = Colorings.colorcode(x)
            all(truth .== res)
        end
    end
end
