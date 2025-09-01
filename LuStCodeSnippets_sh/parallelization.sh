#!/bin/bash

wait_asp(){
    #   - function to control parallelized for loops
    #       - does so in an asynchronous parallel (ASP) manner
    #
    #Usage
    #-----
    #   ```bash
    #   n_running=0
    #   maxjobs=...
    #   for (...); do
    #       (   #subshell for parallelzation via background tasks
    #           <your parallelized tasks>
    #       ) &
    #
    #       ((n_running++)) #increment number of running jobs
    #
    #       wait_asp maxjobs n_running
    #
    #   done
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`maxjobs_loc`)
    #       - `string` (nameref)
    #       - maximum number of jobs to be running simultaneously
    #       - will make sure to have `maxjobs_loc` jobs running at all times
    #           - i.e., as soon as a job finishes, the next job is launched
    #           - except if there are no jobs left
    #   - $2 (`n_running_loc`)
    #       - `string` (nameref)
    #       - number of currently running jobs
    #       - will get modified when calling the function
    #
    #Example
    #-------
    #   ```bash
    #   n_running=0
    #   maxjobs=3
    #   for ((i=0; i<10; i++)); do
    #       (
    #           echo "Task ${i} started"
    #           t=$((RANDOM % 3 + 1))
    #           sleep $t
    #           echo "Task ${i} finished after ${t}"
    #       ) &
    #       ((n_running++))
    #       wait_asp maxjobs n_running
    #   done
    #   wait
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   Task 0 started
    #   Task 1 started
    #   Task 2 started
    #   Task 1 finished after 1
    #   Task 3 started
    #   Task 2 finished after 1
    #   Task 4 started
    #   Task 0 finished after 2
    #   Task 5 started
    #   Task 4 finished after 1
    #   Task 6 started
    #   Task 5 finished after 1
    #   Task 3 finished after 2
    #   Task 7 started
    #   Task 8 started
    #   Task 6 finished after 1
    #   Task 9 started
    #   Task 8 finished after 3
    #   Task 7 finished after 3
    #   Task 9 finished after 3
    #   ```

    local -n maxjobs_loc=$1     #nameref to keep parameters similar
    local -n n_running_loc=$2   #nameref to modify original value

    if (( n_running_loc >= maxjobs_loc )); then #check if maximum number of jobs is exceeded
        wait -n                                 #wait for the next job to finish
        ((n_running_loc--))                     #decrease running counter to launch next job
    fi
}

wait_bsp(){
    #   - function to control parallelized for loops
    #       - does so in an bulk synchronous parallel (BSP) manner
    #
    #Usage
    #-----
    #   ```bash
    #   source _projectbuildingblocks.sh
    #   n_running=0
    #   maxjobs=...
    #   for (...); do
    #       (   #subshell for parallelzation via background tasks
    #           <your parallelized tasks>
    #       ) &
    #
    #       ((n_running++)) #increment number of running jobs
    #
    #       wait_bsp maxjobs n_running
    #
    #   done
    #   ```
    #
    #Parameters
    #----------
    #   - $1 (`maxjobs_loc`)
    #       - `string` (nameref)
    #       - maximum number of jobs running simultaneously
    #       - will wait until all of `maxjobs_loc` jobs are finished before launching the next bulk (`maxjobs_loc` jobs)
    #   - $2 (`n_running_loc`)
    #       - `string` (nameref)
    #       - number of currently running jobs
    #       - will get modified when calling the function
    #
    #Example
    #-------
    #   ```bash
    #   n_running=0
    #   maxjobs=3
    #   for ((i=0; i<10; i++)); do
    #       (
    #           echo "Task ${i} started"
    #           t=$((RANDOM % 3 + 1))
    #           sleep $t
    #           echo "Task ${i} finished after ${t}"
    #       ) &
    #       ((n_running++))
    #       wait_bsp maxjobs n_running
    #   done
    #   wait
    #   ```
    #
    #Output
    #------
    #   ```bash
    #   Task 0 started
    #   Task 1 started
    #   Task 2 started
    #   Task 1 finished after 1
    #   Task 2 finished after 1
    #   Task 0 finished after 1
    #   Task 3 started
    #   Task 4 started
    #   Task 5 started
    #   Task 3 finished after 2
    #   Task 4 finished after 2
    #   Task 5 finished after 2
    #   Task 6 started
    #   Task 7 started
    #   Task 8 started
    #   Task 8 finished after 1
    #   Task 6 finished after 2
    #   Task 7 finished after 2
    #   Task 9 started
    #   Task 9 finished after 3
    #   ```
    
    local -n maxjobs_loc=$1     #nameref to keep parameters similar
    local -n n_running_loc=$2   #nameref to modify original value

    if (( n_running_loc >= maxjobs_loc )); then #check if maximum number of jobs is exceeded
        wait                                    #wait for current bulk (all `maxjobs_loc` jobs) to finish
        n_running_loc=0                         #reset running counter to launch next bulk of `maxjobs_loc` job
    fi
}

#prevent direct execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This is a library file. Source it in your scripts: source <path/to/_projectbuildingblocks.sh>"
fi
