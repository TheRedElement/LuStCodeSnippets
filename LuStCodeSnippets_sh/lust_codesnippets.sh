#!/bin/bash

# - script to `source` all modules

#%%get relevant paths
SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIR="$(dirname $SCRIPT_PATH)"

#%%imports
source "$SCRIPT_DIR/./git_routines.sh"
source "$SCRIPT_DIR/./hypsearch.sh"
source "$SCRIPT_DIR/./makemontage.sh"
source "$SCRIPT_DIR/./parallelization.sh"