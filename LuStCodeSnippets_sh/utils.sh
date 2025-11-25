#!/bin/bash

agent_forwarding () {
    local help='
        - function to setup agent forwarding whenever using ssh
        - will make sure that the ssh keys below are forwarded to the remote server

        Usage
        -----
            ```bash
        	agent_forwarding
        	```

        Parameters
        ----------

        Example
        -------
        	```bash
        	agent_forwarding
        	```

        Output
        ------
        	```
        	Agent pid <some process id>
        	Identity added: <path/to/your/private/key>
        	```

        Comments
        --------
        	- whenever ssh into some remote server call the following to use the forwarded ssh key
        	```bash
        	ssh -A <user>@host
        	```
        	- to test if the forwarding (for github) is setup correctly use
        	```bash
        	ssh -A <user>@host ssh -T git@github.com
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
    else
        ###############
        #FUNCTION BODY#
        ###############

        echo "Setting up agent forwarding for github"
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/github	#forward github sshkey
    fi    
}

calc () {
    local help='
        - function to run calculations with precision point

        Usage
        -----
            ```bash
        	calc "<mexpr>" "scale"
        	```

        Parameters
        ----------
           - $1 (`mexpr`)
               - `expression`
               - math expression to evaluate
           - $2 (`scale`)
               - `int`, optional
               - precision to use for the calculation
        		- the default is `2`
        			- 2 decimals

        Example
        -------
        	```bash
        	calc 3/5 2
            calc "1/(8*2)" 3
        	```

        Output
        ------
        	```bash
        	.75
            .062
        	```

        Comments
        --------
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
	local mexpr="${args[0]}"  		#math expression to evaluate
    local scale="${args[1]:-2}"	    #set scale

    if [[ "${args[0]}" == "--help" ]]; then
        echo "$help"
    else
        ###############
        #FUNCTION BODY#
        ###############

	    echo "scale=$scale; $mexpr" | bc      
    fi        
}

#prevent direct execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This is a library file. Source it in your scripts: source <path/to/_projectbuildingblocks.sh>"
fi
