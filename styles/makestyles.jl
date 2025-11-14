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
        "/* tre.css */",
        "/* load via <link rel=\"stylesheet\" href=path2file> */",
        "\n",
        "/* css variables (can be overridden in html or other css files) */",
    ]
        
    begin #add global variables
        push!(lines, ":root {")
        push!(lines, "$(' '^indent)/* colors */")
        
        begin #colors
            for color in keys(style["colors"])
                if check_context(["all","css"], style["colors"][color]["context"])
                    push!(lines, "$(' '^indent)--$(color): $(style["colors"][color][theme]);")
                end
            end
        end
        begin #text styling
            push!(lines, "$(' '^indent)/* text styling */")
            
        end
        push!(lines, "}\n")
    end

    begin #define elements
        main_body = """
        /* ################################################################## */
        /* GLOBAL DEFAULTS */
        html, body {
            background-color: var(--c_bg);
            color: var(--c_body_text);
        }

        /* ################################################################## */
        /* HEADERS */
        h1 {
            color: var(--c_h1);
            font-size: 1.5rem;
            font-weight: bold;
        }
        h2 {
            color: var(--c_h2);
            font-size: 1.3rem;
            font-weight: bold
        }
        h3 {
            color: var(--c_h3);
            font-size: 1.1rem;
            font-weight: bold
        }
        h4 {
            color: var(--c_h4);
            font-size: 1.0rem;
            font-weight: bold
        }

        /* ################################################################## */
        /* FLOATS */
        /* tables */
        table {
            display: inline-block;
            overflow: hidden;
            counter-increment: tab;
            width: 100%;
            table-layout: auto;
        }
        table :is(th, tr:nth-child(even)) {			/*style all elements in `:is` (th...table header; tr:nth-child(even)...even table rows*/
            background-color: var(--c_bg);
            border: 1px solid var(--c_tabborder);
            padding: 0.3cqi;
        }
        table tbody tr:nth-child(odd) {				/*odd table rows*/
            background-color: var(--c_tabrow_bg);
        }
        table tbody tr:hover td {					/*highlight on hover*/
            background: var(--c_tabrow_hover);
        }
        table td {
            width: 1%;  /* tiny minimum width => browser tries to expand regardless of content*/
        }
        table caption {
            width: 100%;
            display: block;
            text-align: left;
        }
        table caption::before {
            content: "Table " counter(tab) ": ";
            font-weight: bold;
        }
        table tfoot > tr > td {
            border-top: 1px solid;
        }
        table tfoot > tr > td::before {
            content: "Notes: ";
            font-weight: bold;
        }

        /* figures */
        figure {
            display: inline-block;
            overflow: hidden;
            counter-increment: fig;
        }
        figure img {
            width: 100%;    /* because always wrapped in figure */
            height: auto;
            display: block;    
            margin: 0 auto;
        }
        figure figcaption {
            width: 100%;
            display: block;
            text-align: left;
        }
        figure figcaption::before{
            content: "Figure " counter(fig) ": ";
            font-weight: bold;
        }

        /* ################################################################## */
        /* other buliding blocks */
        span.footnote {
            color: var(--c_footnote_text);
            font-size: 0.8rem;
            position: relative;
            cursor: pointer;
            vertical-align: super;
            counter-increment: footnotes;
        }
        span.footnote::before {
            content: counter(footnotes)" ";
            vertical-align: super;
            font-size: 0.8rem;
        }
        span.footnote::after {
            content: attr(data-note);
            position: absolute;
            width: max-content;
            max-width: 15rem;
            background-color: var(--c_footnote_box);
            border-radius: 4px;
            box-shadow: 0 2px 6px var(--c_footnote_boxshadow);
            opacity: 0;
            pointer-events: none;
            transform: translateY(0.5rem);
            transition: opacity 0.15s ease, transform 0.15s ease;    
            z-index: 10;
            white-space: normal;

        }
        span.footnote:hover::after {
            opacity: 1;
            transform: translateY(0);
        }

        blockquote {
            display: inline-block;
            overflow: hidden;
            font-size: 1.2rem;
            text-align: left;
            width: 95%;
            color: var(--c_blockquote_text);
            margin-left: 0.5rem;    
            border-left: 0.5rem var(--c_blockquote_border) solid;
            background-color: var(--c_blockquote_bg);
        }

        /* ################################################################## */
        /* CROSSREFERENCES */
        a:link {
            color: var(--c_link_text);
            background-color: transparent;
            text-decoration: none;
            font-style: italic;
        }

        a:visited {
            color: var(--c_link_visited);
            background-color: transparent;
            text-decoration: none;
            font-style: italic;
        }

        a:hover {
            color: var(--c_link_hover);
            background-color: transparent;
            text-decoration: underline;
            font-style: italic;
        }

        a:active {
            color: var(--c_link_active);
            background-color: transparent;
            text-decoration: underline;
            font-style: italic;
        }

        /* ################################################################## */
        /* LISTS */

        /* ---------------------------------------- */
        /* bullet lists */
        ul {
            font-size: 1rem;
            color: var(--c_list1_text);
        }

        /* custom bullet (red button? */
        /* ul > li:before {	
            content: "🍪 ";
        } */

        ul ul {
            font-size: 1rem;
            color: var(--c_list2_text);
        }

        /* ---------------------------------------- */
        /* ordered lists */
        /* top level */
        ol {
            counter-reset: item;
            list-style: none;
            padding-left: 1.5rem;
        }
        ol > li {
            counter-increment: item;
            color: var(--c_list1_text);
        }
        ol > li::before{
            content: counters(item, ".") ". ";
        }
        li > ol {   /* reset counter when new nested element starts */
            counter-reset: item;
        }

        ol ol {
            font-size: rem;
            color: var(--c_list2_text);
        }
        /* ################################################################## */
        /* ITERATION COMMANDS */
        span.commentLS {
            color: var(--c_commentls);
            text-decoration: underline;
            text-decoration-style: wavy;
            font-style: italic;
        }

        span.commentLS::after {
            content: " [" attr(data-comment) "]";
            text-decoration: none;
        }

        span.todoLS {
            color: var(--c_todols);
            font-style: italic;
        }

        span.todoLS::before {
            content: "[TODO: ";
        }

        span.todoLS::after {
            content: "]";
        }

        /* ################################################################## */
        /* LAYOUTING */
        /* n column layout */
        .columns {
            display: flex;
            gap: 5%;
            width: 100%;
        }
        .column {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            /* outline: 10px solid rgba(0, 0, 0, 0); */
        }

        /* row layout */
        .rows {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            margin-top: 3%;
            /* outline: 1px solid rgb(255, 0, 0, 0); */
        }

        """
        push!(lines, main_body)

        
    end
    
    #generate file
    f = open("tre_$(theme).css", "w")
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
make_css("dark")
make_css("light")
make_latexcolors()