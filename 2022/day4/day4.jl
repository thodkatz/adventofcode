module day4

function parse_range(range)
    start, finish = split(range, "-")
    return (parse(Int64, start), parse(Int64, finish))
end

function parse_line(line)
    first, second = split(line, ",")
    return parse_range(first), parse_range(second)
end

function in(first_range, second_range)
    if size_range(first_range) > size_range(second_range)
        return between(second_range[1], first_range) && between(second_range[2], first_range)
    else
        return between(first_range[1], second_range) && between(first_range[2], second_range)
    end
end

function size_range(range)
    return range[2] - range[1]
end

function between(target, range)
    return range[1] <= target <= range[2]
end

function overlap(first_range, second_range)
    if first_range[1] < second_range[1]
        return between(second_range[1], first_range) || between(second_range[2], first_range)
    else
        return between(first_range[1], second_range) || between(first_range[2], second_range)
    end
end

file = "input.txt"
task1() = count([in(parse_line(line)...) for line in readlines(file)])
task2() = count([overlap(parse_line(line)...) for line in readlines(file)])

println(task1())
println(task2())


end