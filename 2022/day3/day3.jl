module day3

function filtinput(file)
    return [split(line, "") for line in readlines(file)]
end

function calc(first, second)
    common = only(intersect(first, second)[1])
    score = Int(lowercase(common)) - Int('a') + 1
    if isuppercase(common)
        score += 26 
    end
    return score
end

function task1()
    score = 0
    for input = filtinput("input.txt")
        score += calc(input[1:end÷2], input[end÷2+1:end])
    end
    return score
end

function task2()
    score = 0
    input = filtinput("input.txt")
    for i = 1:3:length(input)
        score += calc(intersect(input[i], input[i+1]),input[i+2])
    end
    return score
end


println(task1())
println(task2())

end