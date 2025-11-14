#%%imports
using JSON

#%%definitions
"""
    - function to convert `s` from snake_case to `camelCase`

    Parameters
    ----------
        - `s`
            - `String`
            - string to be converted
    
    Raises
    ------

    Returns
    -------
        - `s_camel`
            - `String`
            - converted version of `s`

    Dependencies
    ------------

    Comments
    --------
"""
function snake2camel(
    s::String
    )::String
    initials = getfield.(eachmatch(r"(?<=\_)\w",s), :match)
    underscores = getfield.(eachmatch(r"\_\w",s),:match)
    s_camel = replace(s, (underscores.=>uppercase.(initials))...)
    return s_camel
end


function check_context(
    contexts::Vector{String}, context_json::Vector{Any},
    )::Bool
    return any(in.(contexts, Ref(context_json))) #only use css context
end
function make_cssroot(
    theme::String="dark",
    indent::Int=4,
    )
    
    #default parameters

    begin #checks
        @assert in(theme, ["dark","light"])
    end

    #read style
    style = JSON.parsefile("tre.json")
    
    #generate css file lines
    lines = []
    push!(lines, "$(' '^indent)/* colors */")
    for color in keys(style["colors"])
        if check_context(["all","css"], style["colors"][color]["context"])
            push!(lines, "$(' '^indent)--$(color): $(style["colors"][color][theme]);")
        end
    end
    
    #generate file
    insert!(lines, 1, ":root {")
    push!(lines, "}")
    f = open("tre.css", "w")
    write(f, join(lines, "\n"))
    close(f)
end

function make_latexcolors(
    theme::String="dark",
    indent::Int=4,
    )
    
    #read style
    style = JSON.parsefile("tre.json")
    
    #generate css file lines
    lines = []
    for color in keys(style["colors"])
        if check_context(["all","latex"], style["colors"][color]["context"])
            line2add = "\\definecolor{$(color)}{HTML}{$(style["colors"][color][theme][2:end])}"
            line2add = snake2camel(line2add)
            push!(lines, line2add)
        end
    end
    
    #generate file
    f = open("tre.sty", "w")
    write(f, join(lines, "\n"))
    close(f)
end

#%%main
make_cssroot()
make_latexcolors()