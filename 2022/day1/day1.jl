#!/usr/bin/julia
module day1

function read()
    input = readlines("input.txt")
    empty_lines = findall(isempty, input)
    calories = getindex.(Ref(input), UnitRange.([1; empty_lines .+ 1], [empty_lines .- 1; length(input)]))
    calories = [parse.(Int64, elf_calories) for elf_calories in calories]
    return calories
end

cals = read()

task1(x) = maximum(sum.(x))
println(task1(cals))

task2(x) = sum(sort(sum.(x), rev=true)[1:3])
println(task2(cals))

end
