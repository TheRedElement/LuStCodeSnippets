#%%imports
using Colors
using Dates
using JSON

#%%definitions
"""
    snake2camel(
        s::String
        )::String

converts `s` from snake_case to `camelCase`

# Arguments
- `s`
    - `String`
    - string to be converted

# Returns
- `s_camel`
    - `String`
    - converted version of `s`

"""
function snake2camel(
    s::String
    )::String
    initials = getfield.(eachmatch(r"(?<=\_)\w",s), :match)
    underscores = getfield.(eachmatch(r"\_\w",s),:match)
    s_camel = replace(s, (underscores.=>uppercase.(initials))...)
    return s_camel
end
"""converts hex to a julia rgb string"""
function hex2rgba_string(hex)
    rgba = parse(RGBA, hex)
    return "rgba($(float(rgba.r)),$(float(rgba.g)),$(float(rgba.b)),$(float(rgba.alpha)))"
end

"""
    check_context(
        contexts::Vector{String}, context_json::Vector{Any},
        )::Bool

checks the context provided in the json style sheet

- used to filter for specific applications (i.e. get all colors relevant for css)

See also
- [`make_css`](@ref)
- [`make_latexcolors`](@ref)

# Arguments
- `contexts`
    - the context to check for
- `context_json`
    - the context specified in the json style sheet

# Returns
- `flag`
    - `Bool`
    - if any of the desired `contexts` are specified in the json style sheet
"""
function check_context(
    contexts::Vector{String}, context_json::Vector{Any},
    )::Bool
    return any(in.(contexts, Ref(context_json)))
end

"""
    make_css(
        indent::Int=4,
        )

generates a css style sheet from `./tre.json`

# Arguments
- `theme`
    - the theme to generate
    - will be used to query color information from the `./tre.json`
- `indent`
    - indentations to use in the generated style sheet


# Extended help

## Dependencies
- [`JSON.parsefile`](@ref)

"""
function make_css(
    indent::Int=4,
    )

    #default parameters

    begin #checks
    end

    #read style
    style = JSON.parsefile("tre.json")

    #init css file
    lines_root = []             #:root
    lines_light = []            #light-mode

    begin #add global variables
        #:root
        theme_root = "dark"
        push!(lines_root, ":root {")
        begin #colors (root)
            push!(lines_root, "$(' '^indent)/* colors */")
            for color in keys(style["colors"])
                if check_context(["all","css"], style["colors"][color]["context"])
                    push!(lines_root, "$(' '^indent)--$(color): $(style["colors"][color][theme_root]);")
                end
            end
        end
        begin #fontsizes
            push!(lines_root, "$(' '^indent)/* fontsizes */")
            for fs in keys(style["fontsizes"])
                if check_context(["all","css"], style["fontsizes"][fs]["context"])
                    push!(lines_root, "$(' '^indent)--$(fs): $(style["fontsizes"][fs]["value"]);")
                end
            end
        end
        push!(lines_root, "}\n")

        #light
        push!(lines_light, "body.tre-light {")
        theme_light = "dark"
        begin #colors (light)
            push!(lines_light, "$(' '^indent)/* colors */")
            for color in keys(style["colors"])
                if check_context(["all","css"], style["colors"][color]["context"])
                    push!(lines_light, "$(' '^indent)--$(color): $(style["colors"][color][theme_light]);")
                end
            end
        end
        push!(lines_light, "}\n")
    end

    #load template and add respective parts
    begin
        main_body = read(open("tre_template.css", "r"), String)
        main_body = replace(main_body, ":root {\n}" => join(lines_root, "\n"))
        main_body = replace(main_body, "body.tre-light {\n}" => join(lines_light, "\n"))
    end

    #generate file
    f = open("tre.css", "w")
    write(f, main_body)
    close(f)
end

"""

generates a `Plots.jl` style sheet template (.json) from `./tre.json`

- will generate files in several locations
    - to make sure the style is accessible also from installed modules
    - all files follow the naming convention tre_PlotsJl.json
    - essentially just copies of `./tre.json` but with substitutions to follow `Plots.jl` naming conventions

# Arguments
- `indent`
    - indentations to use in the generated style sheet

# Extended help

## Dependencies
- [`JSON.parsefile`](@ref)
"""
function make_plots_jl(
    indent::Int=4,
    )
    #read style
    style = JSON.parsefile("tre.json")


    #modification to comply with Plots.jl names
    style["marker"]["symbol"] = Dict(k => replace.(v,
            r"^triangle-up$"=>"utriangle",
            r"^triangle-down$"=>"dtriangle",
            r"^star$"=>"star5",
        ) for (k,v) in style["marker"]["symbol"]
    )
    # style["hatches"] = Dict(k => replace.(v,
    #         "\\"=>"\\\\",
    #     ) for (k,v) in style["hatches"]
    # )


    #save in style in locations where it is needed to be accessible upon module import
    for location in [
            "./",                               #this directory
            "../LuStCodeSnippets_jl/_data/"     #julia package
        ]
        open(joinpath(location, "./tre_PlotsJl.json"), "w") do f
            JSON.print(f, style, indent)
        end
    end
end

"""
    make_latexcolors(
        indent::Int=4,
        )

generates a latex style (.sty) sheet from `./tre.json`

# Arguments
- `indent`
    - indentations to use in the generated style sheet

# Extended help

## Dependencies
- [`JSON.parsefile`](@ref)
"""
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

"""
    make_matplotlib(
        indent::Int=4,
        )

generates a matplotib style sheet template (.json) from `./tre.json`

- will generate files in several locations
    - to make sure the style is accessible also from installed modules
    - all files follow the naming convention tre_matplotlib.json
    - essentially just copies of `./tre.json` but with substitutions to follow matplotlib naming conventions

# Arguments
- `indent`
    - indentations to use in the generated style sheet

# Extended help

## Dependencies
- [`JSON.parsefile`](@ref)
"""
function make_matplotlib(
    indent::Int=4,
    )
    #read style
    style = JSON.parsefile("tre.json")

    #modification to comply with matplotlib names
    style["line"]["dash"] = Dict(k => replace.(v,
        r"^dash$"=>"dashed",
        r"^dot$"=>"dotted",
        r"^dasheddotted$"=>"dashdotted",
        ) for (k,v) in style["line"]["dash"]
    )
    style["marker"]["symbol"] = Dict(k => replace.(v,
            r"^circle$"=>"o",
            r"^square$"=>"s",
            r"^triangle-up$"=>"^",
            r"^triangle-down$"=>"v",
            r"^star$"=>"*",
        ) for (k,v) in style["marker"]["symbol"]
    )

    #save in style in locations where it is needed to be accessible upon module import
    for location in [
            "./",                               #this directory for organization #this directory to be accessible for javascript
            "../lust_codesnippets_py/_data/"    #python package
        ]
        open(joinpath(location, "./tre_matplotlib.json"), "w") do f
            JSON.print(f, style, indent)
        end
    end
end

"""
    make_plotly(
        theme::String="dark",
        cycle::String="cycle",
        indent::Int=4,
        )

generates a plotly style sheet (.json) from `./tre.json`

- will generate files in several locations
    - to make sure the style is accessible also from installed modules
    - all files follow the naming convention tre_plotly_<theme>_<cycle>.json
- generated style can be used with javascript and python

# Arguments
- `theme`
    - the theme to generate
    - will be used to query color information from the `./tre.json`
- `cycle`
    - mode to use for cycling through linestyles, markers, hatches, etc.
    - options are
        - `"cycle"`
            - will cycle through the linestyles
            - every line consecutive line, marker, hatch, etc. will have a unique style
        - `"batch"`
            - will batch similar linestyles together
            - consecutive lines, markes, hatches, etc. will have the same style
- `indent`
    - indentations to use in the generated style sheet

# Extended help

## Dependencies
- [`JSON.parsefile`](@ref)
"""
function make_plotly(
    theme::String="dark",
    cycle::String="cycle",
    indent::Int=4,
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
                            "shape" => style["hatches"][cycle][i]
                        )
                    ),
                ) for i in range(1, length(style["hatches"][cycle]))
            ],
            "scatter" => [
                Dict(
                    "line" => Dict(
                        "width" => style["line"]["width"],
                        "dash" => style["line"]["dash"][cycle][i],
                    ),
                    "marker" => Dict(
                        "size" => style["marker"]["size"],
                        "symbol" => style["marker"]["symbol"][cycle][i],
                    ),
                    "error_x" => style["errorbars"]["error_x"],
                    "error_y" => style["errorbars"]["error_y"],
                ) for i in range(1, min(length(style["line"]["dash"][cycle]),length(style["marker"]["symbol"][cycle])))
            ],
            "heatmap" => [
                Dict(
                    "colorscale" => style["colors"]["c_plot_cmap"][theme],
                ),
            ],
            "surface" => [
                Dict(
                    "colorscale" => style["colors"]["c_plot_cmap"][theme],
                ),
            ],
        ),
        "layout" => Dict(
            #sorted alphabetically
            "autosize" => style["figure"]["autosize"],
            "coloraxis" => Dict(
                "colorbar" => Dict(
                    "outlinewidth" => style["axes"]["coloraxis"]["colorbar"]["outlinewidth"],
                )
            ),
            "colorscale" => Dict(   #not working in js
                "sequential" => style["colors"]["c_plot_cmap"][theme],
                "sequentialminus" => style["colors"]["c_plot_cmap"][theme],
                "diverging" => style["colors"]["c_plot_cmap"][theme],
            ),
            "colorway" => style["colors"]["c_plot_colorway"][theme],
            "font" => Dict(
                "color" => style["colors"]["c_body_text"][theme],
                "size" => style["fontsizes"]["fs_plot_body"]["value"],
            ),
            "legend" => Dict(
                "bgcolor" => style["colors"]["c_plot_legendbg"][theme],
                "bordercolor" => style["colors"]["c_plot_legendborder"][theme],
                "itemwidth" => style["legend"]["itemwidth"],
                "orientation" => style["legend"]["orientation"],
                "x" => style["legend"]["x"],
                "xanchor" => style["legend"]["xanchor"],
                "y" => style["legend"]["y"],
                "yanchor" => style["legend"]["yanchor"],
            ),
            "height" => style["figure"]["height"],
            "margin" => style["figure"]["margin"],
            "paper_bgcolor" => style["colors"]["c_bg"][theme],
            "plot_bgcolor" => style["colors"]["c_plot_pane"][theme],
            "scene" => Dict(
                "zaxis" => Dict(
                    "color" => style["colors"]["c_body_text"][theme],
                    "gridcolor" => style["colors"]["c_plot_grid"][theme],
                    "linecolor" => style["colors"]["c_body_text"][theme],
                    "showgrid" => style["axes"]["xaxis"]["showgrid"],
                    "showline" => style["axes"]["xaxis"]["showline"],
                    "ticks" => "inside",
                    "visible" => style["axes"]["xaxis"]["visible"],
                    "zeroline" => style["axes"]["xaxis"]["zeroline"],
                ),
            ),
            "width" => style["figure"]["width"],
            "xaxis" => Dict(
                "automargin" => style["axes"]["xaxis"]["automargin"],
                "color" => style["colors"]["c_body_text"][theme],
                "gridcolor" => style["colors"]["c_plot_grid"][theme],
                "linecolor" => style["colors"]["c_body_text"][theme],
                "minor" => Dict(
                    "ticks" => "inside",
                ),
                "showgrid" => style["axes"]["xaxis"]["showgrid"],
                "showline" => style["axes"]["xaxis"]["showline"],
                "side" => style["axes"]["xaxis"]["spines"][1],
                "ticks" => "inside",
                "visible" => style["axes"]["xaxis"]["visible"],
                "zeroline" => style["axes"]["xaxis"]["zeroline"],
            ),
            "yaxis" => Dict(
                "automargin" => style["axes"]["yaxis"]["automargin"],
                "color" => style["colors"]["c_body_text"][theme],
                "gridcolor" => style["colors"]["c_plot_grid"][theme],
                "linecolor" => style["colors"]["c_body_text"][theme],
                "minor" => Dict(
                    "ticks" => "inside",
                ),
                "showgrid" => style["axes"]["yaxis"]["showgrid"],
                "showline" => style["axes"]["yaxis"]["showline"],
                "side" => style["axes"]["yaxis"]["spines"][1],
                "ticks" => "inside",
                "visible" => style["axes"]["yaxis"]["visible"],
                "zeroline" => style["axes"]["yaxis"]["zeroline"],
            ),
        )
    )

    #save in style in locations where it is needed to be accessible upon module import
    for location in [
            "./",                               #this directory for organization #this directory to be accessible for javascript
            "../lust_codesnippets_py/_data/"    #python package
        ]
        open(joinpath(location, "./tre_plotly_$(theme)_$(cycle).json"), "w") do f
            JSON.print(f, data, indent)
        end
    end
end




#%%main
themes = ["dark", "light"]
cycles = ["cycle", "batch"]
make_css()
make_plots_jl()
make_latexcolors()
make_matplotlib()
for theme in themes
    for cycle in cycles
        make_plotly(theme, cycle)
    end
end
