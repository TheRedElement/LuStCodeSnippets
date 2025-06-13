
unlink_submodule() {
    #   - function to unlik a git submodule
    #
    #Usage
    #-----
    #   ```bash
    #   unlink_submodule <submodule_path> <do_commit>
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`submodule_path`)
    #       - `string`
    #       - path to the submodule to unlink
    #   - $2 (`do_commit`)
    #       - `bool`, optional
    #       -  whether to add and commit the changes after unlinking the submodule
    #
    #Example
    #-------
    #   ```bash
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   ```    
    local submodule_path="$1"
    local do_commit="${2:-true}"  #default is "yes" if not specified

    #check if enough arguments are provided
    if [ -z "$submodule_path" ]; then
        echo "Usage: unlink_submodule <submodule_path> [do_commit]"
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
