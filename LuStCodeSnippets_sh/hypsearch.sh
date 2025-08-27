#!/bin/bash

#%%definitions
carthesian_product() {
    #   - function to compute the Cartesian product of multiple arrays
    #       - generates all possible combinations (Cartesian product) of elements from multiple arrays
    #       - uses recursion to efficiently handle any number of arrays
    #
    #Usage
    #-----
    #   ```bash
    #   combine "" out_arr arr1[@] arr2[@] arr3[@]
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`prefix`)
    #       - `string`
    #       - prefix for the current combination (initially empty)
    #   - $2 (`out_arr`)
    #       - `array`
    #       -  output array to be used as objects to store result in
    #   - $3+ (`arr1` `arr2` ...)
    #       - `array` `array` ...
    #       - references to bash arrays containing elements to combine
    #
    #Example
    #-------
    #   ```bash
    #   declare -a out_arr
    #   arr1=(a b)
    #   arr2=(1 2)
    #   arr3=(X Y)
    #   carthesian_product "" out_arr arr1[@] arr2[@] arr3[@]
    #
    #   for combo in "${result_array[@]}"; do
    #       echo "[$combo]"
    #   done
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   [a 1 X ]
    #   [a 1 Y ]
    #   [a 2 X ]
    #   [a 2 Y ]
    #   [b 1 X ]
    #   [b 1 Y ]
    #   [b 2 X ]
    #   [b 2 Y ]
    #   ```
    
    local prefix="${1:-}"   #current combination of elements (initially empty)
    local out_arr=$2        #get name of output array (not a reference yet) 
    shift 2                 #shift left twice to process the next array (skip out_arr and first input)
        
    #base case
    ##if no more arrays are left, print the result and return
    if [[ $# -eq 0 ]]; then     #`$#` represents number of arguments
        eval "$out_arr+=(\"\$prefix\")"     #append current prefix (use indirect reference to modify `out_arr` in place)
        return
    fi

    #retrieve the next array using indirect reference
    local arr=("${!1}")     #"${!1}" dereferences array name in $1
    shift                   #move to the next argument

    #iterate over each element in the current array
    for val in "${arr[@]}"; do
        #recursively call the function with updated prefix
        carthesian_product "$prefix$val " "$out_arr" "$@"       #pass name of `out_arr` as string (to avoid circular references)
    done
}

get_random_indices() {
    #   - function to generate an array of random, nonrepeating indices
    #
    #Usage
    #-----
    #   ```bash
    #   source _projectbuildingblocks.sh
    #   ridxs=($(get_random_indices N K))
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`N`)
    #       - maximum number to sample
    #           - largest index
    #           - length of arrat to be indexed
    #   - $2 (`K`)
    #       - number of elements to sample without replacement
    #       - will be set to `N` in case `K > N`
    #
    #Example
    #-------
    #   ```bash
    #   ridxs=($(get_random_indices 10 5))     #indices to random subset of all hyperparameter combinations for current job (random indices without replacement)
    #   echo "${ridxs[@]}"
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   8 6 4 1 9
    #   ```

    local N=$1  #get parameters
    local K=$2  #get parameters
    
    K=$(( K > N ? N : K ))      #make sure `K` os always smaller than `N`
    shuf -i 0-$(($N-1)) -n $K   #randomly shuffle range and select first `K` elements
}

#prevent direct execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This is a library file. Source it in your scripts: source <path/to/_projectbuildingblocks.sh>"
fi
