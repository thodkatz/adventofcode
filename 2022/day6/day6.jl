function day6(line, distinct)
    chars = Dict()
    start = 1
    for (count, c) in enumerate(line)
        if (count - start) == distinct
            return count - 1
        elseif haskey(chars, c) && chars[c] >= start
            start = chars[c] + 1
        end
        chars[c] = count
    end
end

for line = readlines("input.txt")
    println(day6(line, 4))
    println(day6(line, 14))
end