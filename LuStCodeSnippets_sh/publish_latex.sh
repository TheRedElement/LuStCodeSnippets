#!/bin/bash
#%%definitions
publish_latex () {

    local help='
        - compiles a publishable version of a paper
        - will
            - create a new directory `${outdir}`
            - copy the original source file (`${infile}.tex) to a new, publishable file `${outdir}/${outfile}.tex`
            - copy bib-refs.bib to `${outdir}`
            - copy the bib-style (`.bst`) to `${outdir}`
            - include the glossary (from `./glossary.tex`) in the `${outdir}/${outfile}.tex`
            - remove all comments in the `${outdir}/${outfile}.tex`
            - extract all figures (patterns matching `\includegraphics[...]{...}`) in order of appearing in `${infile}`
            - rename figures in sequence of appearance (`fig<i>_<figname>.pdf`)
            - move those renamed figures to `${outdir}`
            - compile the latex file in the `${outdir}` directory
            - remove unnecessary auxiliary files
            - zip the contents of `${outdir}` to have an archive for publication


        Usage
        ```bash
        publish_latex <infile> <outfile> [outdir=<outdir>]
        ```

        Parameters
            - `infile`
                - str
                - filename of the input file WITHOUT EXTENSION
                - `infile` has to be located in the current directory
            - `outfile`
                - str
                - filename of the publishable output file WITHOUT EXTENSION
            - `outdir`
                - str, kwarg, optional
                - output directory to use for the publishable version
                - has to end in a slash (`/`)
                - the default is `outdir=submission/`

        Example
        ```bash
        publish_latex LStein Steinwender2026_LStein outdir=submission/
        ```

        Output
        ```bash
        ```
    '

    ################
    #DEAL WITH ARGS#
    ################
    declare -a args=()  #positional args via array
    declare -A kwargs=( #emulate named kwargs via associative array
        [outdir]="submission/"
    )
    for arg in "$@"; do
        if [[ "$arg" == *=* ]]; then    #check if arg contains an `=` (kwargs)
            key="${arg%%=*}"            #name (before `=`)
            val="${arg#*=}"             #value (after `=`)
            kwargs[$key]="$val"         #override default
        else                            #interpret as positional
            args+=("$arg")
        fi
    done

    #default values for positional args
    local infile="${args[0]}"
    local outfile="${args[1]}"

    if [[ "${args[0]}" == "--help" ]]; then
        echo "$help"
    else
        ###############
        #FUNCTION BODY#
        ###############

        echo $"called publish_latex" \
            "${infile} ${outfile}" \
            "outdir=${kwargs[outdir]}"

        #extract figures
        ##get all `\includegraphics[...]{...}` with contents`
        ##extract contents from `{...}`
        ##get filename and extension
        ##convert to bash array
        mapfile -t figures < <(
            grep -oP '\\includegraphics(?:\[[^]]*\])?{[^}]+}' ${infile}.tex \
            | grep -oP '(?<={)[^}]+' \
            | grep -oP '(?<=gfx\/)\w+\.\w+$'
        )

        # printf "%s\n" "${figures[@]}"

        #init submission directory
        mkdir -p ${kwargs[outdir]};

        #init submittable file
        cp "${infile}.tex" "${kwargs[outdir]}${outfile}.tex";

        #include bib-refs
        cp bib-refs.bib "${kwargs[outdir]}/bib-refs.bib"
        cp *.bst "${kwargs[outdir]}/"

        #include latex class
        cp *.cls "${kwargs[outdir]}/"

        #include glossary
        sed -i '/\input{glossary}/r glossary.tex' "${kwargs[outdir]}${outfile}.tex";
        sed -i -E '/\\input\{glossary\}/d' "${kwargs[outdir]}${outfile}.tex";

        #remove all comments
        sed -i -E '/^\s*%/d' "${kwargs[outdir]}${outfile}.tex";                 #deletes commented lines (also indented ones)
        sed -i -E 's/(^|[^\\])%.*$/\1/' "${kwargs[outdir]}${outfile}.tex";      #deletes line from (non-escaped) comment symbol onward #`\1` adds back matched prefix to not delete that character

        #rename figures
        for ((i=0; i<${#figures}; i++)); do
            cp "gfx/${figures[i]}" "./${kwargs[outdir]}/fig$((i+0))_${figures[i]}";
            sed -i -E "s/gfx\/${figures[i]}/fig$((i+0))_${figures[i]}/" "${kwargs[outdir]}${outfile}.tex";
        done

        #only operate in outdir (do not touch original directory)
        cd "${kwargs[outdir]}"

        #compile (4x to ensure `autonum`, `cleveref`, etc. resolve correctly)
        pdflatex -interaction=nonstopmode "${outfile}.tex"  #1st pass (creates `.aux` for bibtex + glossary files)
        bibtex "${outfile}"                                 #run BibTeX (uses `.aux`)
        makeglossaries "${outfile}"                         #run makeglossaries
        pdflatex -interaction=nonstopmode "${outfile}.tex"  #2nd pass (incorporates bibliography + glossary)
        pdflatex -interaction=nonstopmode "${outfile}.tex"  #3rd pass (fix cross-references, cleveref, etc.)


                #remove unnecessary auxiliary files
        # rm -f *.bbl
        rm -f *.acn *.acr *.alg *.aux *.bcf *.blg *.fdb_latexmk *.fls *.glg *.glo *.gls *.ist *.log *.out *.spl *.toc     #keep `.bbl` for arxiv

        #for journal
        #-----------
        #zip latex source
        rm "${outfile}_LatexSource.zip"
        zip -r "${outfile}_LatexSource" *.bib *.bst *.cls *.tex fig*_*.*

        #for arxiv
        #---------
        rm ax.tar
        tar -cvvf ax.tar *.tex *.bst *.bbl *.cls fig*_*.*  #compress for upload to arxiv (only upload files that are necessary for compilation)

        #go back to previous directory
        cd -
    fi
}
