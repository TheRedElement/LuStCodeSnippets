#%%imports
using Colors
using Dates
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
function hex2rgba_string(hex)
    rgba = parse(RGBA, hex)
    return "rgba($(float(rgba.r)),$(float(rgba.g)),$(float(rgba.b)),$(float(rgba.alpha)))"
end


function check_context(
    contexts::Vector{String}, context_json::Vector{Any},
    )::Bool
    return any(in.(contexts, Ref(context_json))) #only use css context
end

function make_css(
    theme::String="dark",
    indent::Int=4,
    )
    
    #default parameters

    begin #checks
        @assert in(theme, ["dark","light"])
    end

    #read style
    style = JSON.parsefile("tre.json")
    
    #init css file
    lines = [
    ]
        
    begin #add global variables
        push!(lines, ":root {")
        
        begin #colors
            push!(lines, "$(' '^indent)/* colors */")
            for color in keys(style["colors"])
                if check_context(["all","css"], style["colors"][color]["context"])
                    push!(lines, "$(' '^indent)--$(color): $(style["colors"][color][theme]);")
                end
            end
        end
        begin #fontsizes
            push!(lines, "$(' '^indent)/* fontsizes */")
            for fs in keys(style["fontsizes"])
                if check_context(["all","css"], style["fontsizes"][fs]["context"])
                    push!(lines, "$(' '^indent)--$(fs): $(style["fontsizes"][fs]["value"]);")
                end
            end
        end
        push!(lines, "}\n")
    end

    #load template and add respective parts
    begin
        main_body = read(open("tre_template.css", "r"), String)
        main_body = replace(main_body, ":root {\n}" => join(lines, "\n"))
        main_body = replace(main_body, "\$(theme)" => theme)
    end

    #generate file
    f = open("tre_$(theme).css", "w")
    write(f, main_body)
    close(f)
end

function make_latexcolors(
    indent::Int=4,
    )
    
    #read style
    style = JSON.parsefile("tre.json")
    
    begin #define file head
        head = """
        %Template by Steinwender Lukas

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %- Package providing user defined colors
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        %==============================================================
        %Identification:
        %The package identifies itself and the LaTeX version needed

        \\NeedsTeXFormat{LaTeX2e}
        \\ProvidesPackage{TRE}[$(today()) v1.0 Colors for the document following the red element style.]

        %==============================================================
        %Require packages and preliminary definitions needed
        \\RequirePackage{xcolor}               %for colors
        \\RequirePackage{ifthen}               %for if-else

        %==============================================================
        %Handle options that might be passed to the package

        %option for selecting the theme
        %------------------------------
        \\DeclareOption{light}{\\newcommand{\\usetheme}{light}}
        \\DeclareOption{dark}{\\newcommand{\\usetheme}{dark}}
        \\DeclareOption*{\\PackageError{TRE}
                                        {Unknown '\\CurrentOption'!
                                        Allowed are:
                                        'light' or 'dark'!}
                                        {Consider changing the options you passed to
                                        'light' or 'dark'.}
                        }
        \\ProcessOptions\\relax


        %==============================================================
        \\ifthenelse{\\equal{\\usetheme}{light}}\
        """        
    end

    #generate css file lines
    lines = [head]
    begin #dark theme
        push!(lines, "{%colors for light theme")
        for color in keys(style["colors"])
            if check_context(["all","latex"], style["colors"][color]["context"])
                line2add = "$(" "^indent)\\definecolor{$(color)}{HTML}{$(uppercase(style["colors"][color]["light"][2:end-2]))}"
                line2add = snake2camel(line2add)
                push!(lines, line2add)
            end
        end
        push!(lines, "}")
    end
    begin #light theme
        push!(lines, "{%colors for dark theme")
        for color in keys(style["colors"])
            if check_context(["all","latex"], style["colors"][color]["context"])
                line2add = "$(" "^indent)\\definecolor{$(color)}{HTML}{$(uppercase(style["colors"][color]["dark"][2:end-2]))}"
                line2add = snake2camel(line2add)
                push!(lines, line2add)
            end
        end
        push!(lines, "}")
    end
    
    f = open("TRE.sty", "w")
    write(f, join(lines, "\n"))
    close(f)
end

function make_plotly(
    theme::String="dark",
    indent::Int=2,
    )
    #read style
    style = JSON.parsefile("tre.json")


    data = Dict(
        "data" => Dict(
            #sorted alphabetically
            "histogram" => [
                Dict(
                    "marker" => Dict(
                        "pattern" => Dict(
                            "shape" => style["hatches"]["cycle"][i]
                        )
                    ),
                ) for i in range(1, length(style["hatches"]["cycle"]))
            ],
            "scatter" => [
                Dict(
                    "line" => Dict(
                        "width" => 5,
                        "dash" => style["linestyles"]["cycle"][i],
                    ),
                    "marker" => Dict(
                        "size" => 15,
                        "symbol" => style["markers"]["cycle"][i],
                    )
                ) for i in range(1, min(length(style["linestyles"]["cycle"]),length(style["markers"]["cycle"])))
            ],            
        ),
        "layout" => Dict(
            #sorted alphabetically
            "coloraxis" => Dict(
                "colorbar" => Dict(
                    "outlinewidth" => 5,
                )
            ),
            "colorscale" => Dict(   #not working in js
                "sequential" => "plasma",
                "sequentialminus" => "plasma",
                "diverging" => [
                    [0, "#000000"],
                    [0.5, "#f7f7f7"],
                    [1, "#b40426"]
                ],
            ),
            "colorway" => [
                style["colors"]["c_plot_c0"][theme],
                style["colors"]["c_plot_c1"][theme],
                style["colors"]["c_plot_c2"][theme],
                style["colors"]["c_plot_c3"][theme],
            ],
            "font" => Dict(
                "color" => style["colors"]["c_body_text"][theme],
                "size" => style["fontsizes"]["fs_plot_body"]["value"],
            ),
            "legend" => Dict(
                "itemwidth" => 80,
                "bgcolor" => style["colors"]["c_plot_legendbg"][theme],
            ),            
            "margin" => Dict("t" =>0, "b" =>10, "l" =>100, "r" =>0),
            "paper_bgcolor" => style["colors"]["c_bg"][theme],
            "plot_bgcolor" => style["colors"]["c_plot_pane"][theme],
            "scene" => Dict(
                "zaxis" => Dict(
                    "visible" => true,
                    "showline" => true,
                    "zeroline" => false,
                    "color" => style["colors"]["c_body_text"][theme],
                    "linecolor" => style["colors"]["c_body_text"][theme],
                    "gridcolor" => style["colors"]["c_plot_gridcolor"][theme],
                ),                  
            ),
            "xaxis" => Dict(
                "visible" => true,
                "showline" => true,
                "zeroline" => false,
                "automargin" => true,
                "color" => style["colors"]["c_body_text"][theme],
                "linecolor" => style["colors"]["c_body_text"][theme],
                "gridcolor" => style["colors"]["c_plot_gridcolor"][theme],
            ),
            "yaxis" => Dict(
                "visible" => true,
                "showline" => true,
                "zeroline" => false,
                "automargin" => true,
                "color" => style["colors"]["c_body_text"][theme],
                "linecolor" => style["colors"]["c_body_text"][theme],
                "gridcolor" => style["colors"]["c_plot_gridcolor"][theme],
            ),
        )
    )

    #save in style submodule to have everything in one place upon import
    open("../lust_codesnippets_py/styles/tre_$(theme)_plotly.json", "w") do f
        JSON.print(f, data, indent)
    end

end

#%%main
# make_css("dark")
# make_css("light")
# make_latexcolors()
make_plotly("dark")
make_plotly("light")