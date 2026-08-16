#!/bin/bash

git_log() {
    local help='
        prints prettified version of `git log` in the terminal

        - formatting similar to a git graph

        Usage
        ```bash
        git_log
        ```

        Parameters

        Example
        ```bash
        git_log
        ```

        Output
        ```bash
        [...]
        ```
    '

    ################
    #DEAL WITH ARGS#
    ################
    declare -a args=()  #positional args via array
    declare -A kwargs=( #emulate named kwargs via associative array
        #no kwargs
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
    if [[ "${args[0]}" == "--help" ]]; then
        echo "$help"
        return 0
    fi

    ############### #FUNCTION BODY#
    ###############

    echo $"called git_log" \
        ""

    git log --graph --oneline --decorate --all --color
}

rm_gitignored() {
    local help='
        deletes all files in the current directory that are gitignored

        Usage
        ```bash
        rm_gitignored
        ```

        Parameters

        Example
        ```bash
        rm_gitignored
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
        #no kwargs
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
    if [[ "${args[0]}" == "--help" ]]; then
        echo "$help"
        return 0
    fi

    ###############
    #FUNCTION BODY#
    ###############

    echo $"called rm_gitignored" \
        ""

    git check-ignore *.* | xargs -r rm -v
}

unlink_submodule() {
    local help='
        unliks a git submodule

        Usage
        ```bash
        unlink_submodule <submodule_path> [do_commit]
        ```

        Parameters
        - $1 (`submodule_path`)
            - `string`
            - path to the submodule to unlink
        - $2 (`do_commit`)
            - `bool`, optional
            -  whether to add and commit the changes after unlinking the submodule

        Example
        ```bash
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
        #no kwargs
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
    local submodule_path="${args[0]}"
    local do_commit="${args[1]:-true}"

    if [[ "${args[0]}" == "--help" ]]; then
        echo "$help"
        return 0
    fi

    ###############
    #FUNCTION BODY#
    ###############

    echo $"called unlink_submodule" \
        "${submodule_path} ${do_commit}"


    #check if enough arguments are provided
    if [ -z "$submodule_path" ]; then
        echo "not enough arguments: unlink_submodule <submodule_path> [do_commit]"
        return 1
    fi

    #ask user to confirm
    read -p "Unlink submodule at '$submodule_path'? [y/N]: " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        return 1
    fi
    echo "Unlinking submodule at '$submodule_path'..."

    #remove submodule entry from .gitmodules
    git config -f .gitmodules --remove-section "submodule.$submodule_path"

    #remove submodule entry from .git/config
    git config -f .git/config --remove-section "submodule.$submodule_path"

    #unstage the submodule
    git rm --cached "$submodule_path"

    #delete the submodule's .git directory if it exists
    rm -rf "$submodule_path/.git"

    #optionally add and commit the result
    if [ "$do_commit" = true ]; then
        git add "$submodule_path"
        git commit -m "Convert submodule '$submodule_path' to regular directory"
        echo "Submodule '$submodule_path' has been unlinked and committed as a regular directory."
    else
        echo "Submodule '$submodule_path' has been unlinked. Add and commit manually if needed."
    fi
}


#prevent direct execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This is a library file. Source it in your scripts: source <path/to/_projectbuildingblocks.sh>"
fi
