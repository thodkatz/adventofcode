module day2

@enum result WIN=6 DRAW=3 LOSE=0
@enum signs ROCK=1 PAPER=2 SCISSORS=3
sign_intepret = Dict('A' => ROCK, 'B' => PAPER, 'C' => SCISSORS)
towin = Dict(ROCK => PAPER, PAPER => SCISSORS, SCISSORS => ROCK)
tolose = Dict(ROCK => SCISSORS, PAPER => ROCK, SCISSORS => PAPER)


function task1()
    score = 0
    for line = readlines("input.txt")
        me_intepret = Dict('X' => ROCK, 'Y' => PAPER, 'Z' => SCISSORS)
        you, me = filter(x -> !isspace(x), line)
        you, me = sign_intepret[you], me_intepret[me]
        if towin[you] == me
            score += Int(WIN)
        elseif tolose[you] == me
            score += Int(LOSE)
        elseif you == me
            score += Int(DRAW)
        else
            throw(DomainError(me, "unexpected sign"))
        end
        score += Int(me)
    end
    return score
end

function task2()
    score = 0
    for line = readlines("input.txt")
        me_intepret = Dict('X' => LOSE, 'Y' => DRAW, 'Z' => WIN)
        you, me = filter(x -> !isspace(x), line)
        you, me = sign_intepret[you], me_intepret[me]
        if me == WIN
            score += Int(towin[you])
        elseif me == DRAW
            score += Int(you)
        elseif me == LOSE
            score += Int(tolose[you])
        else
            throw(DomainError(me, "unexpected sign"))
        end
        score += Int(me)
    end
    return score
end

println(task1())
println(task2())

end
